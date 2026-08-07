"""
Extended Covariate Extraction for Shock Index Acute Abdomen Study
Extract: Lactate, WBC, Hemoglobin, Creatinine (from labevents)
         Vasopressor use (from inputevents)
         Surgical procedures (from procedures_icd)
         Ventilation status (from chartevents)
"""
import pandas as pd, numpy as np, os, sys, time

base = 'E:/mimic-iv/v3.1/physionet.org/files/mimiciv/3.1'
out_dir = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'

# Load our analysis cohort
df = pd.read_csv(os.path.join(out_dir, 'analysis_dataset.csv'))
cohort_hadm = set(df['hadm_id'].values)
cohort_stay = set(df['stay_id'].values)
cohort_subject = set(df['subject_id'].values)
print(f'Cohort: {len(df)} stays, {len(cohort_hadm)} hadm_ids, {len(cohort_subject)} subjects')

# ============================================================
# 1. LABEVENTS: Lactate, WBC, Hb, Creatinine
# ============================================================
lab_itemids = {
    50813: 'lactate',       # Blood Gas Lactate
    53154: 'lactate',       # Chemistry Lactate (backup)
    52442: 'lactate',       # Blood Gas Lactate (backup)
    51301: 'wbc',           # White Blood Cells
    51300: 'wbc_count',     # WBC Count
    50811: 'hemoglobin',    # Hemoglobin Blood Gas
    50912: 'creatinine',    # Creatinine Chemistry
}
target_lab_items = set(lab_itemids.keys())

print('\n=== Extracting Lab Events (chunked) ===')
lab_results = []
chunk_size = 1_000_000
total_chunks = 0
start_time = time.time()

for chunk in pd.read_csv(os.path.join(base, 'hosp/labevents.csv.gz'), 
                          chunksize=chunk_size,
                          usecols=['subject_id','hadm_id','itemid','charttime','value','valuenum','ref_range_lower','ref_range_upper']):
    total_chunks += 1
    # Filter: our cohort + target itemids
    mask = chunk['hadm_id'].isin(cohort_hadm) & chunk['itemid'].isin(target_lab_items)
    filtered = chunk[mask].copy()
    if len(filtered) > 0:
        # Add variable name
        filtered['var_name'] = filtered['itemid'].map(lab_itemids)
        lab_results.append(filtered)
    
    if total_chunks % 50 == 0:
        elapsed = time.time() - start_time
        print(f'  Chunk {total_chunks}, elapsed: {elapsed:.0f}s, collected: {sum(len(r) for r in lab_results)} records')

print(f'  Total chunks: {total_chunks}, time: {time.time()-start_time:.0f}s')

# Combine lab results
lab_df = pd.concat(lab_results, ignore_index=True)
print(f'Lab records for cohort: {len(lab_df)}')

# Process lab values
lab_df['valuenum'] = pd.to_numeric(lab_df['valuenum'], errors='coerce')
lab_df = lab_df[lab_df['valuenum'].notna() & (lab_df['valuenum'] > 0)].copy()

# For variables with multiple itemids, merge names
# lactate: combine 50813, 53154, 52442
# wbc: use 51301 primarily, 51300 as backup
lab_df['var_name'] = lab_df['itemid'].map(lab_itemids)

# Get first value and mean within 24h of ICU admission for each hadm_id
# We need ICU intime to compute 24h window - load from icustays
icu_stays = pd.read_csv(os.path.join(base, 'icu/icustays.csv.gz'))
icu_stays['intime'] = pd.to_datetime(icu_stays['intime'])
icu_stays_24h = icu_stays[icu_stays['stay_id'].isin(cohort_stay)][['stay_id','hadm_id','intime']].copy()

lab_df['charttime_dt'] = pd.to_datetime(lab_df['charttime'], errors='coerce')
lab_df = lab_df.merge(icu_stays_24h, on='hadm_id', how='left')

# Compute hours from ICU intime
lab_df['hours_from_icu'] = (lab_df['charttime_dt'] - lab_df['intime']).dt.total_seconds() / 3600

# Filter: within first 24h of ICU
lab_24h = lab_df[(lab_df['hours_from_icu'] >= -2) & (lab_df['hours_from_icu'] <= 24)].copy()
print(f'Lab records within 24h of ICU: {len(lab_24h)}')

# Aggregate: first value, mean, max within 24h per stay_id per variable
lab_agg = lab_24h.groupby(['stay_id', 'var_name']).agg(
    first_val=('valuenum', 'first'),
    mean_val=('valuenum', 'mean'),
    max_val=('valuenum', 'max'),
    min_val=('valuenum', 'min')
).reset_index()

# For lactate, combine all sources
lac_agg = lab_agg[lab_agg['var_name'] == 'lactate'].groupby('stay_id').agg(
    lactate_first=('first_val', 'min'),   # take minimum first value across sources
    lactate_mean=('mean_val', 'mean'),
    lactate_max=('max_val', 'max')
).reset_index()

# For WBC, prioritize 51301
wbc_agg = lab_agg[lab_agg['var_name'] == 'wbc'].groupby('stay_id').agg(
    wbc_first=('first_val', 'first'),
    wbc_mean=('mean_val', 'mean'),
    wbc_max=('max_val', 'max')
).reset_index()

# For hemoglobin
hb_agg = lab_agg[lab_agg['var_name'] == 'hemoglobin'].groupby('stay_id').agg(
    hb_first=('first_val', 'first'),
    hb_mean=('mean_val', 'mean'),
    hb_min=('min_val', 'min')
).reset_index()

# For creatinine
cr_agg = lab_agg[lab_agg['var_name'] == 'creatinine'].groupby('stay_id').agg(
    cr_first=('first_val', 'first'),
    cr_mean=('mean_val', 'mean'),
    cr_max=('max_val', 'max')
).reset_index()

# Save individual lab summaries
col_prefix_map = {'lactate': 'lactate', 'wbc': 'wbc', 'hemoglobin': 'hb', 'creatinine': 'cr'}
for name, agg_df in [('lactate', lac_agg), ('wbc', wbc_agg), ('hemoglobin', hb_agg), ('creatinine', cr_agg)]:
    prefix = col_prefix_map[name]
    first_col = f'{prefix}_first'
    print(f'{name}: {len(agg_df)} stays with data')
    if first_col in agg_df.columns:
        print(f'  {first_col}: median={agg_df[first_col].median():.2f}, range=[{agg_df[first_col].min():.2f}, {agg_df[first_col].max():.2f}]')
    else:
        print(f'  Columns: {list(agg_df.columns)}')

# ============================================================
# 2. VASOPRESSOR USE from inputevents
# ============================================================
vaso_itemids = {
    221906: 'norepinephrine',
    221289: 'epinephrine',
    221662: 'dopamine',
    221653: 'dobutamine',
    222315: 'vasopressin',
    221749: 'phenylephrine',
    221986: 'milrinone',
}

print('\n=== Extracting Vasopressor Use ===')
vaso_results = []
chunk_size_vaso = 500_000

for chunk in pd.read_csv(os.path.join(base, 'icu/inputevents.csv.gz'),
                          chunksize=chunk_size_vaso,
                          usecols=['subject_id','hadm_id','stay_id','itemid','starttime','endtime','rate','amount','ordercategoryname','statusdescription']):
    mask = chunk['stay_id'].isin(cohort_stay) & chunk['itemid'].isin(vaso_itemids.keys())
    filtered = chunk[mask].copy()
    if len(filtered) > 0:
        filtered['vaso_name'] = filtered['itemid'].map(vaso_itemids)
        vaso_results.append(filtered)

if len(vaso_results) > 0:
    vaso_df = pd.concat(vaso_results, ignore_index=True)
    print(f'Vasopressor records: {len(vaso_df)}')
    
    # Determine vasopressor use (any dose > 0)
    vaso_df['rate'] = pd.to_numeric(vaso_df['rate'], errors='coerce')
    vaso_df['amount'] = pd.to_numeric(vaso_df['amount'], errors='coerce')
    
    # Binary: any vasopressor use within 24h of ICU admission
    vaso_used = vaso_df[vaso_df['rate'] > 0].copy()
    vaso_stays = vaso_used['stay_id'].unique()
    
    # Which specific vasopressors
    vaso_type_agg = vaso_used.groupby('stay_id')['vaso_name'].apply(set).reset_index()
    vaso_type_agg.columns = ['stay_id', 'vaso_types']
    
    print(f'Stays with vasopressor use: {len(vaso_stays)} ({len(vaso_stays)/len(cohort_stay)*100:.1f}%)')
    
    # Vaso duration within 24h
    vaso_used['starttime_dt'] = pd.to_datetime(vaso_used['starttime'], errors='coerce')
    vaso_used['endtime_dt'] = pd.to_datetime(vaso_used['endtime'], errors='coerce')
    vaso_used = vaso_used.merge(icu_stays_24h[['stay_id','intime']], on='stay_id', how='left')
    vaso_used['hours_from_icu'] = (vaso_used['starttime_dt'] - vaso_used['intime']).dt.total_seconds() / 3600
    
    # Filter to first 24h
    vaso_24h = vaso_used[(vaso_used['hours_from_icu'] >= 0) & (vaso_used['hours_from_icu'] <= 24)].copy()
    vaso_24h['duration_hours'] = (vaso_24h['endtime_dt'] - vaso_24h['starttime_dt']).dt.total_seconds() / 3600
    vaso_24h['duration_hours'] = vaso_24h['duration_hours'].clip(upper=24)
    
    vaso_duration = vaso_24h.groupby('stay_id')['duration_hours'].sum().reset_index()
    vaso_duration.columns = ['stay_id', 'vaso_duration_hours']
    
    # Norepinephrine specifically
    ne_used = vaso_24h[vaso_24h['vaso_name'] == 'norepinephrine']['stay_id'].unique()
    
else:
    print('No vasopressor records found for cohort')
    vaso_stays = np.array([])
    vaso_type_agg = pd.DataFrame(columns=['stay_id', 'vaso_types'])
    vaso_duration = pd.DataFrame(columns=['stay_id', 'vaso_duration_hours'])
    ne_used = np.array([])

# ============================================================
# 3. SURGICAL PROCEDURES from procedures_icd
# ============================================================
print('\n=== Extracting Surgical Procedures ===')
proc = pd.read_csv(os.path.join(base, 'hosp/procedures_icd.csv.gz'))
proc_cohort = proc[proc['hadm_id'].isin(cohort_hadm)].copy()
print(f'Procedure records for cohort: {len(proc_cohort)}')

# Define abdominal surgery ICD codes
# ICD-9: laparotomy 54.x, appendectomy 47.x, cholecystectomy 51.x, bowel resection 45.x, hernia repair 53.x
# ICD-10: similar procedure codes
def is_abdominal_surgery(icd_code, icd_version):
    code = str(icd_code).strip()
    if icd_version == 9:
        prefixes = ['54','47','51','45','53','44','46','48','49','52','55','56','57','62']
        for p in prefixes:
            if code.startswith(p):
                return True
    elif icd_version == 10:
        prefixes = ['0DJ','0FB','0FT','0JP','0JH','0UT','0WJ','0FK','0FD','0DN']
        # Also check simpler prefixes
        for prefix in ['0D','0F','0J','0U','0W']:
            if code.startswith(prefix):
                return True
    return False

# Emergency surgery flag
def is_emergency_surgery(icd_code, icd_version):
    code = str(icd_code).strip()
    # Specific emergency abdominal procedure codes
    if icd_version == 9:
        emergency_codes = ['540','541','542','5491','5492',  # appendectomy
                           '511','512','513',  # cholecystectomy
                           '450','451','452','453',  # bowel resection
                           '549',  # other laparotomy
                           ]
        for ec in emergency_codes:
            if code.startswith(ec):
                return True
    return False

proc_cohort['abdominal_surgery'] = proc_cohort.apply(
    lambda r: is_abdominal_surgery(r['icd_code'], r['icd_version']), axis=1)
proc_cohort['emergency_surgery'] = proc_cohort.apply(
    lambda r: is_emergency_surgery(r['icd_code'], r['icd_version']), axis=1)

# Aggregate per hadm_id
surgery_agg = proc_cohort.groupby('hadm_id').agg(
    any_surgery=('abdominal_surgery', 'max'),
    emergency_surgery=('emergency_surgery', 'max'),
    total_procedures=('seq_num', 'count')
).reset_index()

surgery_agg['any_surgery'] = surgery_agg['any_surgery'].astype(int)
surgery_agg['emergency_surgery'] = surgery_agg['emergency_surgery'].astype(int)

print(f'Hadm with abdominal surgery: {surgery_agg["any_surgery"].sum()}')
print(f'Hadm with emergency surgery: {surgery_agg["emergency_surgery"].sum()}')

# ============================================================
# 4. VENTILATION from chartevents (brief check)
# ============================================================
print('\n=== Extracting Ventilation Status ===')
vent_itemids = [225448, 225449, 225450, 225451, 225452, 225453, 225454, 225455, 224938]  # ventilator settings

# Use a simpler approach: check if ventilation duration exists in concepts
vent_concepts_path = os.path.join(base, 'concepts')
if os.path.exists(vent_concepts_path):
    print(f'Concepts directory exists: {vent_concepts_path}')
    # Check for ventilation related files
    for f in os.listdir(vent_concepts_path):
        if 'vent' in f.lower():
            print(f'  Found: {f}')
else:
    print('No concepts directory - will use chartevents for ventilation')

# Quick ventilation extraction from chartevents using existing full vitals data
# We already have icu_vitals_full.csv, just need to add vent settings
# For simplicity, use invasive ventilation as binary flag based on airway itemids
vent_results = []
chunk_size_vent = 1_000_000

for chunk in pd.read_csv(os.path.join(base, 'icu/chartevents.csv.gz'),
                          chunksize=chunk_size_vent,
                          usecols=['stay_id','itemid','charttime','value']):
    mask = chunk['stay_id'].isin(cohort_stay) & chunk['itemid'].isin(vent_itemids)
    filtered = chunk[mask]
    if len(filtered) > 0:
        vent_results.append(filtered)

if len(vent_results) > 0:
    vent_df = pd.concat(vent_results, ignore_index=True)
    vent_stays = vent_df['stay_id'].unique()
    print(f'Stays with ventilation records: {len(vent_stays)} ({len(vent_stays)/len(cohort_stay)*100:.1f}%)')
else:
    vent_stays = np.array([])
    print('No ventilation records found')

# ============================================================
# 5. MERGE ALL INTO ANALYSIS DATASET
# ============================================================
print('\n=== Merging Extended Covariates ===')

# Start with existing dataset
df_ext = df.copy()

# Add lactate
df_ext = df_ext.merge(lac_agg, on='stay_id', how='left')
print(f'Lactate coverage: {df_ext["lactate_first"].notna().sum()} / {len(df_ext)} ({df_ext["lactate_first"].notna().mean()*100:.1f}%)')

# Add WBC
df_ext = df_ext.merge(wbc_agg, on='stay_id', how='left')
print(f'WBC coverage: {df_ext["wbc_first"].notna().sum()} / {len(df_ext)} ({df_ext["wbc_first"].notna().mean()*100:.1f}%)')

# Add hemoglobin
df_ext = df_ext.merge(hb_agg, on='stay_id', how='left')
print(f'Hemoglobin coverage: {df_ext["hb_first"].notna().sum()} / {len(df_ext)} ({df_ext["hb_first"].notna().mean()*100:.1f}%)')

# Add creatinine
df_ext = df_ext.merge(cr_agg, on='stay_id', how='left')
print(f'Creatinine coverage: {df_ext["cr_first"].notna().sum()} / {len(df_ext)} ({df_ext["cr_first"].notna().mean()*100:.1f}%)')

# Add vasopressor
df_ext['vasopressor_use'] = df_ext['stay_id'].isin(vaso_stays).astype(int)
df_ext = df_ext.merge(vaso_duration, on='stay_id', how='left')
df_ext['norepinephrine_use'] = df_ext['stay_id'].isin(ne_used).astype(int)
print(f'Vasopressor coverage: {df_ext["vasopressor_use"].sum()} / {len(df_ext)} ({df_ext["vasopressor_use"].mean()*100:.1f}%)')

# Add surgery
# Need to map stay_id -> hadm_id (already in dataset)
df_ext = df_ext.merge(surgery_agg, on='hadm_id', how='left')
df_ext['any_surgery'] = df_ext['any_surgery'].fillna(0).astype(int)
df_ext['emergency_surgery'] = df_ext['emergency_surgery'].fillna(0).astype(int)
df_ext['total_procedures'] = df_ext['total_procedures'].fillna(0).astype(int)
print(f'Surgery coverage: {df_ext["any_surgery"].sum()} / {len(df_ext)} ({df_ext["any_surgery"].mean()*100:.1f}%)')

# Add ventilation
df_ext['mechanical_ventilation'] = df_ext['stay_id'].isin(vent_stays).astype(int)
print(f'Mechanical ventilation: {df_ext["mechanical_ventilation"].sum()} / {len(df_ext)} ({df_ext["mechanical_ventilation"].mean()*100:.1f}%)')

# Save extended dataset
df_ext.to_csv(os.path.join(out_dir, 'analysis_dataset_extended.csv'), index=False)
print(f'\nSaved extended dataset: {len(df_ext)} rows, {len(df_ext.columns)} columns')
print(f'Columns: {sorted(df_ext.columns.tolist())}')

# Print summary statistics for new variables
print('\n=== New Variable Summary ===')
for col in ['lactate_first','lactate_max','wbc_first','hb_first','cr_first',
            'vasopressor_use','norepinephrine_use','any_surgery','emergency_surgery',
            'mechanical_ventilation']:
    if col in df_ext.columns:
        if df_ext[col].dtype in ['float64','int64']:
            valid = df_ext[col].notna().sum()
            if df_ext[col].nunique() <= 2:
                print(f'{col}: {valid} valid, {df_ext[col].mean()*100:.1f}% positive')
            else:
                print(f'{col}: {valid} valid, median={df_ext[col].median():.2f}, range=[{df_ext[col].min():.2f}, {df_ext[col].max():.2f}]')
