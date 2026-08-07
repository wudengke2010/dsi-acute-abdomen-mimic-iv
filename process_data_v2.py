"""
Updated data processing: use full chartevents extraction for complete vitals.
Computes Shock Index derivatives, classifies subtypes, CCI.
"""
import pandas as pd, numpy as np, os

OUT = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'
BASE = 'E:/mimic-iv/v3.1/physionet.org/files/mimiciv/3.1'

print('=== Step 1: Build ICU acute abdomen cohort ===')
cohort = pd.read_csv(os.path.join(OUT, 'cohort_admissions.csv'))
icu = pd.read_csv(os.path.join(BASE, 'icu/icustays.csv.gz'))
icu_cohort = icu[icu['hadm_id'].isin(set(cohort['hadm_id']))].copy()
icu_first = icu_cohort.sort_values('intime').groupby('hadm_id').first().reset_index()
print(f'First ICU stays: {len(icu_first)}')

icu_cohort_df = icu_first.merge(
    cohort[['subject_id','hadm_id','gender','anchor_age','anchor_year',
            'admittime','dischtime','deathtime','hospital_expire_flag',
            'admission_type','insurance','race','age_at_admission',
            'edregtime','edouttime','icu_admission','hospital_death']],
    on=['subject_id','hadm_id'], how='left'
)
icu_cohort_df['icu_death'] = icu_cohort_df['hospital_expire_flag'].astype(int)
icu_cohort_df['prolonged_icu'] = (icu_cohort_df['los'] > 3).astype(int)

print(f'ICU death rate: {icu_cohort_df["icu_death"].mean():.3f}')
print(f'Prolonged ICU: {icu_cohort_df["prolonged_icu"].mean():.3f}')

print('\n=== Step 2: Compute Shock Index derivatives (using FULL vitals) ===')

# Check which vitals file exists (full or partial)
vitals_full_path = os.path.join(OUT, 'icu_vitals_full.csv')
vitals_partial_path = os.path.join(OUT, 'icu_vitals.csv')

if os.path.exists(vitals_full_path):
    print('Using FULL vitals extraction')
    vitals = pd.read_csv(vitals_full_path)
else:
    print('Using partial vitals extraction (200 chunks)')
    vitals = pd.read_csv(vitals_partial_path)

vitals['charttime_dt'] = pd.to_datetime(vitals['charttime'])
icu_intime = icu_cohort_df[['stay_id','intime']].copy()
icu_intime['intime_dt'] = pd.to_datetime(icu_intime['intime'])

vitals_merged = vitals.merge(icu_intime, on='stay_id', how='left')
vitals_merged['hours_from_icu'] = (vitals_merged['charttime_dt'] - vitals_merged['intime_dt']).dt.total_seconds() / 3600
vitals_24h = vitals_merged[(vitals_merged['hours_from_icu'] >= 0) & (vitals_merged['hours_from_icu'] <= 24)].copy()
print(f'Vitals within 24h: {len(vitals_24h)} stays covered: {vitals_24h["stay_id"].nunique()}')

# Consolidate BP + HR per stay_id per charttime
# Arterial BP preferred over NIBP
bp_sources = {}
for source in ['arterial', 'nibp', 'art_line']:
    sbp_col = f'SBP_{source}'
    dbp_col = f'DBP_{source}'
    map_col = f'MAP_{source}'
    for vital_type, col_name in [('SBP', sbp_col), ('DBP', dbp_col), ('MAP', map_col)]:
        vals = vitals_24h[vitals_24h['vital_label'] == col_name][['stay_id','charttime','valuenum']].copy()
        vals = vals.rename(columns={'valuenum': vital_type})
        if vital_type in bp_sources:
            bp_sources[vital_type] = pd.concat([bp_sources[vital_type], vals])
        else:
            bp_sources[vital_type] = vals

# Merge SBP, DBP, MAP per stay+time (prefer arterial)
bp_all = bp_sources['SBP'].merge(bp_sources['DBP'], on=['stay_id','charttime'], how='outer')
bp_all = bp_all.merge(bp_sources['MAP'], on=['stay_id','charttime'], how='outer')

# For each stay+time, if both arterial and NIBP exist, keep arterial (lower seq_num typically)
# Since we merged, duplicates may exist - take mean per stay+time
bp_agg = bp_all.groupby(['stay_id','charttime'])[['SBP','DBP','MAP']].mean().reset_index()

# HR
hr = vitals_24h[vitals_24h['vital_label'] == 'Heart_Rate'][['stay_id','charttime','valuenum']].copy()
hr = hr.rename(columns={'valuenum': 'HR'})
hr_agg = hr.groupby(['stay_id','charttime'])['HR'].mean().reset_index()

# RR and SpO2
rr = vitals_24h[vitals_24h['vital_label'] == 'Respiratory_Rate'][['stay_id','charttime','valuenum']].copy()
rr = rr.rename(columns={'valuenum': 'RR'})
rr_agg = rr.groupby(['stay_id','charttime'])['RR'].mean().reset_index()

spo2 = vitals_24h[vitals_24h['vital_label'] == 'SpO2'][['stay_id','charttime','valuenum']].copy()
spo2 = spo2.rename(columns={'valuenum': 'SpO2'})
spo2_agg = spo2.groupby(['stay_id','charttime'])['SpO2'].mean().reset_index()

# Merge all vitals per stay+time
all_vitals = bp_agg.merge(hr_agg, on=['stay_id','charttime'], how='inner')
all_vitals = all_vitals.merge(rr_agg, on=['stay_id','charttime'], how='left')
all_vitals = all_vitals.merge(spo2_agg, on=['stay_id','charttime'], how='left')

# Compute MAP from SBP/DBP if missing
all_vitals['MAP_calc'] = (2*all_vitals['DBP'] + all_vitals['SBP']) / 3
all_vitals['MAP'] = all_vitals['MAP'].fillna(all_vitals['MAP_calc'])

# Physiological filtering
all_vitals = all_vitals[
    (all_vitals['HR'] >= 20) & (all_vitals['HR'] <= 300) &
    (all_vitals['SBP'] >= 40) & (all_vitals['SBP'] <= 300) &
    (all_vitals['DBP'] >= 20) & (all_vitals['DBP'] <= 200) &
    (all_vitals['MAP'] >= 20) & (all_vitals['MAP'] <= 200)
].copy()
print(f'After physiological filtering: {len(all_vitals)} records, {all_vitals["stay_id"].nunique()} stays')

# Compute SI derivatives
all_vitals['SI'] = all_vitals['HR'] / all_vitals['SBP']
all_vitals['MSI'] = all_vitals['HR'] / all_vitals['MAP']
all_vitals['DSI'] = all_vitals['HR'] / all_vitals['DBP']

# Aggregate to stay level
agg_funcs = {
    'HR': ['first', 'max', 'mean'],
    'SBP': ['first', 'min', 'mean'],
    'DBP': ['first', 'min', 'mean'],
    'MAP': ['first', 'min', 'mean'],
    'SI': ['first', 'max', 'mean'],
    'MSI': ['first', 'max', 'mean'],
    'DSI': ['first', 'max', 'mean'],
    'RR': ['first', 'mean'],
    'SpO2': ['first', 'min', 'mean'],
}

stay_vitals = all_vitals.groupby('stay_id').agg(agg_funcs)
stay_vitals.columns = [f'{col}_{func}' for col, func in stay_vitals.columns]
stay_vitals = stay_vitals.reset_index()
print(f'Stay-level vitals: {len(stay_vitals)}')

# Merge with cohort info
stay_vitals_merged = stay_vitals.merge(
    icu_cohort_df[['stay_id','subject_id','hadm_id','age_at_admission','gender',
                   'icu_death','prolonged_icu','los','hospital_death',
                   'admission_type','insurance','race','first_careunit']],
    on='stay_id', how='left'
)

# Compute Age-SI
stay_vitals_merged['Age_SI_first'] = stay_vitals_merged['SI_first'] * (stay_vitals_merged['age_at_admission'] / 10)
stay_vitals_merged['Age_SI_max'] = stay_vitals_merged['SI_max'] * (stay_vitals_merged['age_at_admission'] / 10)
stay_vitals_merged['Age_SI_mean'] = stay_vitals_merged['SI_mean'] * (stay_vitals_merged['age_at_admission'] / 10)

print(f'With SI: {stay_vitals_merged["SI_first"].notna().sum()}')
print(f'ICU death: {stay_vitals_merged["icu_death"].sum()} ({stay_vitals_merged["icu_death"].mean():.3f})')

print('\n=== Step 3: Classify subtypes ===')
diag = pd.read_csv(os.path.join(BASE, 'hosp/diagnoses_icd.csv.gz'))
hadm_set = set(stay_vitals_merged['hadm_id'])
diag_cohort = diag[diag['hadm_id'].isin(hadm_set)].copy()

def classify_subtype(icd_code, icd_version):
    code = str(icd_code).strip()
    if icd_version == 10:
        if any(code.startswith(p) for p in ['K352','K353','K251','K252','K261','K262','K271','K272','K281','K282','K631','K570','K571','K650']):
            return 'perforation'
        if any(code.startswith(p) for p in ['K56','K400','K401','K410','K411','K440','K441','K450','K451','K460']):
            return 'obstruction'
        if code.startswith('K550'):
            return 'ischemia'
        if any(code.startswith(p) for p in ['K35','K36','K37','K80','K81','K85','K860','K861','K573','K574','K651','K652','K653','K659','K831','K832','K833']):
            return 'inflammation'
    elif icd_version == 9:
        if any(code.startswith(p) for p in ['5400','5401','5311','5312','5321','5322','5331','5332','5341','5342','56983','5700','5701','5670']):
            return 'perforation'
        if code.startswith('560') or any(code.startswith(p) for p in ['5500','5501','5520','5521','5530','5531']):
            return 'obstruction'
        if code.startswith('5570'):
            return 'ischemia'
        if any(code.startswith(p) for p in ['5409','541','542','5740','5741','5750','5751','5770','5771','5620','5621','5671','5672','5678','5679']):
            return 'inflammation'
    return 'other'

diag_cohort['subtype'] = diag_cohort.apply(lambda r: classify_subtype(r['icd_code'], r['icd_version']), axis=1)

subtype_by_hadm = diag_cohort.groupby('hadm_id')['subtype'].apply(
    lambda x: 'perforation' if 'perforation' in x.values
    else 'ischemia' if 'ischemia' in x.values
    else 'obstruction' if 'obstruction' in x.values
    else 'inflammation' if 'inflammation' in x.values
    else 'other'
).reset_index()
subtype_by_hadm.columns = ['hadm_id', 'abdomen_subtype']

stay_vitals_merged = stay_vitals_merged.merge(subtype_by_hadm, on='hadm_id', how='left')
stay_vitals_merged['abdomen_subtype'] = stay_vitals_merged['abdomen_subtype'].fillna('other')

print(f'Subtype distribution:')
print(stay_vitals_merged['abdomen_subtype'].value_counts().to_string())

print('\n=== Step 4: Compute CCI ===')
# Simplified CCI computation (same as before but vectorized for speed)
def compute_cci_fast(diag_df, hadm_ids):
    cci_data = []
    diag_by_hadm = diag_df[diag_df['hadm_id'].isin(hadm_ids)].groupby('hadm_id')

    cci_weights = {
        'MI': (1, {'icd10': ['I21','I22','I252'], 'icd9': ['410','412']}),
        'CHF': (1, {'icd10': ['I50','I429'], 'icd9': ['428']}),
        'PVD': (1, {'icd10': ['I70','I71','I73'], 'icd9': ['440','441','443']}),
        'CVD': (1, {'icd10': ['I60','I61','I63','I64','I69'], 'icd9': ['430','431','432','433','434','436']}),
        'Dementia': (1, {'icd10': ['F00','F01','F02','F03','G30'], 'icd9': ['290']}),
        'COPD': (1, {'icd10': ['J40','J41','J42','J43','J44','J45'], 'icd9': ['490','491','492','493']}),
        'Rheumatic': (1, {'icd10': ['M05','M06','M32','M34'], 'icd9': ['710','714','725']}),
        'PUD': (1, {'icd10': ['K25','K26','K27','K28'], 'icd9': ['531','532','533','534']}),
        'LiverMild': (1, {'icd10': ['B18','K70','K71','K73','K74','K76'], 'icd9': ['070','571','573']}),
        'DM': (1, {'icd10': ['E10','E11','E13','E14'], 'icd9': ['2500','2501','2502','2503']}),
        'DMComp': (2, {'icd10': ['E102','E112','E132'], 'icd9': ['2504','2505','2506']}),
        'LiverSevere': (3, {'icd10': ['K704','K721','K760','K761'], 'icd9': ['572']}),
        'Renal': (2, {'icd10': ['N18','N19','I12','I13'], 'icd9': ['582','583','585','586']}),
        'Cancer': (2, {'icd10': ['C'], 'icd9': ['140','141','142','143','144','145','146','147','148','149','150','151','152','153','154','155','156','157','158','159','160','161','162','163','164','165','166','167','168','169','170','171','172','174','175','176','179','180','181','182','183','184','185','186','187','188','189','190','191','192','193','194','195','200','201','202','203']}),
        'Metastatic': (6, {'icd10': ['C77','C78','C79','C80'], 'icd9': ['196','197','198','199']}),
    }

    for hadm_id in hadm_ids:
        try:
            codes = diag_by_hadm.get_group(hadm_id)
        except:
            cci_data.append({'hadm_id': hadm_id, 'CCI': 0})
            continue

        cci = 0
        codes_str = codes.apply(lambda r: (str(r['icd_code']).strip(), r['icd_version']), axis=1).tolist()

        for comp, (weight, prefixes) in cci_weights.items():
            found = False
            for code_str, icd_ver in codes_str:
                key = f'icd{int(icd_ver)}'
                if key in prefixes:
                    for prefix in prefixes[key]:
                        if code_str.startswith(prefix):
                            found = True
                            break
                if found:
                    break
            if found:
                cci += weight

        cci_data.append({'hadm_id': hadm_id, 'CCI': cci})

    return pd.DataFrame(cci_data)

hadm_list = stay_vitals_merged['hadm_id'].unique()
cci_df = compute_cci_fast(diag, hadm_list)
print(f'CCI: mean={cci_df["CCI"].mean():.2f}')

stay_vitals_merged = stay_vitals_merged.merge(cci_df, on='hadm_id', how='left')
stay_vitals_merged.to_csv(os.path.join(OUT, 'analysis_dataset.csv'), index=False)

print(f'\n=== FINAL DATASET ===')
print(f'Total: {len(stay_vitals_merged)}')
print(f'ICU death: {stay_vitals_merged["icu_death"].sum()} ({stay_vitals_merged["icu_death"].mean():.3f})')
print(f'Subtypes:')
print(stay_vitals_merged['abdomen_subtype'].value_counts().to_string())
