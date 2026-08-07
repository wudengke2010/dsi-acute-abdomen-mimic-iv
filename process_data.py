"""
Comprehensive data processing: compute Shock Index derivatives, classify abdomen subtypes,
build final analysis dataset for acute abdomen ICU cohort.
"""
import pandas as pd, numpy as np, os, sys

OUT = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'
BASE = 'E:/mimic-iv/v3.1/physionet.org/files/mimiciv/3.1'

print('=== Step 1: Build ICU acute abdomen cohort ===')

# Load cohort admissions
cohort = pd.read_csv(os.path.join(OUT, 'cohort_admissions.csv'))

# Load ICU stays for our cohort
icu = pd.read_csv(os.path.join(BASE, 'icu/icustays.csv.gz'))
icu_cohort = icu[icu['hadm_id'].isin(set(cohort['hadm_id']))].copy()

# Keep first ICU stay per hadm_id
icu_first = icu_cohort.sort_values('intime').groupby('hadm_id').first().reset_index()
print(f'First ICU stays for cohort: {len(icu_first)}')

# Merge with cohort info
icu_cohort_df = icu_first.merge(
    cohort[['subject_id','hadm_id','gender','anchor_age','anchor_year',
            'admittime','dischtime','deathtime','hospital_expire_flag',
            'admission_type','insurance','race','age_at_admission',
            'edregtime','edouttime','icu_admission','hospital_death']],
    on=['subject_id','hadm_id'], how='left'
)
print(f'ICU cohort with admission info: {len(icu_cohort_df)}')

# Compute ICU LOS
icu_cohort_df['intime_dt'] = pd.to_datetime(icu_cohort_df['intime'])
icu_cohort_df['outtime_dt'] = pd.to_datetime(icu_cohort_df['outtime'])
icu_cohort_df['icu_los_days'] = icu_cohort_df['los']  # already in days in MIMIC-IV

# Outcome: ICU mortality (death during ICU stay or within hospital)
icu_cohort_df['icu_death'] = icu_cohort_df['hospital_expire_flag'].astype(int)

# Outcome: prolonged ICU stay (>3 days)
icu_cohort_df['prolonged_icu'] = (icu_cohort_df['icu_los_days'] > 3).astype(int)

print(f'ICU death rate: {icu_cohort_df["icu_death"].mean():.3f}')
print(f'Prolonged ICU (>3d): {icu_cohort_df["prolonged_icu"].mean():.3f}')
print(f'ICU LOS median: {icu_cohort_df["icu_los_days"].median():.2f}')

print('\n=== Step 2: Compute Shock Index derivatives ===')

# Load ICU vitals
vitals = pd.read_csv(os.path.join(OUT, 'icu_vitals.csv'))
vitals['charttime_dt'] = pd.to_datetime(vitals['charttime'])

# Merge with ICU stay info to compute time from ICU admission
icu_intime = icu_cohort_df[['stay_id','intime_dt']].copy()
vitals_merged = vitals.merge(icu_intime, on='stay_id', how='left')
vitals_merged['hours_from_icu'] = (vitals_merged['charttime_dt'] - vitals_merged['intime_dt']).dt.total_seconds() / 3600

# Filter: within 24h of ICU admission
vitals_24h = vitals_merged[(vitals_merged['hours_from_icu'] >= 0) & (vitals_merged['hours_from_icu'] <= 24)].copy()
print(f'Vitals within 24h of ICU admission: {len(vitals_24h)}')

# Consolidate BP: prefer arterial over NIBP, merge
# For each stay_id + charttime, get best SBP/DBP/MAP
def consolidate_bp(vitals_df):
    """Consolidate BP measurements - prefer arterial line over NIBP"""
    # Arterial BP (most reliable)
    art_sbp = vitals_df[vitals_df['vital_label'] == 'SBP_arterial'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'SBP'})
    art_dbp = vitals_df[vitals_df['vital_label'] == 'DBP_arterial'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'DBP'})
    art_map = vitals_df[vitals_df['vital_label'] == 'MAP_arterial'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'MAP'})

    # NIBP (non-invasive)
    nibp_sbp = vitals_df[vitals_df['vital_label'] == 'SBP_nibp'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'SBP'})
    nibp_dbp = vitals_df[vitals_df['vital_label'] == 'DBP_nibp'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'DBP'})
    nibp_map = vitals_df[vitals_df['vital_label'] == 'MAP_nibp'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'MAP'})

    # Merge arterial with NIBP (arterial preferred)
    bp = art_sbp.merge(art_dbp, on=['stay_id','charttime'], how='outer')
    bp = bp.merge(art_map, on=['stay_id','charttime'], how='outer')
    bp_art = bp.copy()
    bp_art['bp_source'] = 'arterial'

    bp2 = nibp_sbp.merge(nibp_dbp, on=['stay_id','charttime'], how='outer')
    bp2 = bp2.merge(nibp_map, on=['stay_id','charttime'], how='outer')
    bp2['bp_source'] = 'nibp'

    # Combine: for each stay+time, prefer arterial
    bp_all = pd.concat([bp_art, bp2])
    bp_all = bp_all.sort_values(['stay_id','charttime','bp_source'])
    # Keep arterial if available, else NIBP
    bp_all = bp_all.groupby(['stay_id','charttime']).first().reset_index()

    # HR
    hr = vitals_df[vitals_df['vital_label'] == 'Heart_Rate'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'HR'})

    # RR and SpO2
    rr = vitals_df[vitals_df['vital_label'] == 'Respiratory_Rate'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'RR'})
    spo2 = vitals_df[vitals_df['vital_label'] == 'SpO2'][['stay_id','charttime','valuenum']].rename(columns={'valuenum':'SpO2'})

    # Merge all
    result = bp_all.merge(hr, on=['stay_id','charttime'], how='outer')
    result = result.merge(rr, on=['stay_id','charttime'], how='outer')
    result = result.merge(spo2, on=['stay_id','charttime'], how='outer')

    # Compute MAP from SBP/DBP if MAP is missing
    result['MAP_calc'] = (2*result['DBP'] + result['SBP']) / 3
    result['MAP'] = result['MAP'].fillna(result['MAP_calc'])

    return result

bp_hr = consolidate_bp(vitals_24h)
print(f'Consolidated BP+HR records: {len(bp_hr)}')
print(f'Stays with data: {bp_hr["stay_id"].nunique()}')

# Remove physiologically impossible values
bp_hr = bp_hr[
    (bp_hr['HR'] >= 20) & (bp_hr['HR'] <= 300) &
    (bp_hr['SBP'] >= 40) & (bp_hr['SBP'] <= 300) &
    (bp_hr['DBP'] >= 20) & (bp_hr['DBP'] <= 200) &
    (bp_hr['MAP'] >= 20) & (bp_hr['MAP'] <= 200)
].copy()
print(f'After physiological filtering: {len(bp_hr)}')

# Compute Shock Index derivatives for each measurement
bp_hr['SI'] = bp_hr['HR'] / bp_hr['SBP']
bp_hr['MSI'] = bp_hr['HR'] / bp_hr['MAP']
bp_hr['DSI'] = bp_hr['HR'] / bp_hr['DBP']

print(f'\nSI stats: mean={bp_hr["SI"].mean():.3f}, median={bp_hr["SI"].median():.3f}')
print(f'MSI stats: mean={bp_hr["MSI"].mean():.3f}, median={bp_hr["MSI"].median():.3f}')
print(f'DSI stats: mean={bp_hr["DSI"].mean():.3f}, median={bp_hr["DSI"].median():.3f}')

# Aggregate to stay-level: first value, worst value (max SI), mean value
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

stay_vitals = bp_hr.groupby('stay_id').agg(agg_funcs)
# Flatten column names
stay_vitals.columns = [f'{col}_{func}' for col, func in stay_vitals.columns]
stay_vitals = stay_vitals.reset_index()
print(f'Stay-level vitals: {len(stay_vitals)}')

# Merge Age-SI
stay_vitals_merged = stay_vitals.merge(
    icu_cohort_df[['stay_id','subject_id','hadm_id','age_at_admission','gender',
                   'icu_death','prolonged_icu','icu_los_days','hospital_death',
                   'admission_type','insurance','race','first_careunit']],
    on='stay_id', how='left'
)

# Compute Age-adjusted SI
stay_vitals_merged['Age_SI_first'] = stay_vitals_merged['SI_first'] * (stay_vitals_merged['age_at_admission'] / 10)
stay_vitals_merged['Age_SI_max'] = stay_vitals_merged['SI_max'] * (stay_vitals_merged['age_at_admission'] / 10)
stay_vitals_merged['Age_SI_mean'] = stay_vitals_merged['SI_mean'] * (stay_vitals_merged['age_at_admission'] / 10)

print(f'\nFinal analysis dataset: {len(stay_vitals_merged)} stays')
print(f'With complete SI data: {stay_vitals_merged["SI_first"].notna().sum()}')
print(f'ICU death rate: {stay_vitals_merged["icu_death"].mean():.3f}')
print(f'Hospital death rate: {stay_vitals_merged["hospital_death"].mean():.3f}')

print('\n=== Step 3: Classify acute abdomen subtypes ===')

# Load diagnoses for our cohort
diag = pd.read_csv(os.path.join(BASE, 'hosp/diagnoses_icd.csv.gz'))
cohort_hadm_set = set(stay_vitals_merged['hadm_id'])
diag_cohort = diag[diag['hadm_id'].isin(cohort_hadm_set)].copy()

# Classify abdomen subtype
def classify_subtype(icd_code, icd_version):
    code = str(icd_code).strip()
    if icd_version == 10:
        # Perforation type
        if any(code.startswith(p) for p in ['K352','K353','K251','K252','K261','K262','K271','K272','K281','K282','K631','K570','K571','K650']):
            return 'perforation'
        # Obstruction type
        if any(code.startswith(p) for p in ['K56','K400','K401','K410','K411','K440','K441','K450','K451','K460']):
            return 'obstruction'
        # Ischemia type
        if code.startswith('K550'):
            return 'ischemia'
        # Inflammation type (biliary, pancreatitis, appendicitis non-perforation, diverticulitis non-perforation)
        if any(code.startswith(p) for p in ['K35','K36','K37','K80','K81','K85','K860','K861','K573','K574','K651','K652','K653','K659','K831','K832','K833']):
            return 'inflammation'
    elif icd_version == 9:
        # Perforation
        if any(code.startswith(p) for p in ['5400','5401','5311','5312','5321','5322','5331','5332','5341','5342','56983','5700','5701','5670']):
            return 'perforation'
        # Obstruction
        if code.startswith('560') or any(code.startswith(p) for p in ['5500','5501','5520','5521','5530','5531']):
            return 'obstruction'
        # Ischemia
        if code.startswith('5570'):
            return 'ischemia'
        # Inflammation
        if any(code.startswith(p) for p in ['5409','541','542','5740','5741','5750','5751','5770','5771','5620','5621','5671','5672','5678','5679']):
            return 'inflammation'
    return 'other'

diag_cohort['subtype'] = diag_cohort.apply(lambda r: classify_subtype(r['icd_code'], r['icd_version']), axis=1)

# For each hadm_id, determine primary subtype (from seq_num=1 diagnosis or most severe)
subtype_by_hadm = diag_cohort.groupby('hadm_id')['subtype'].apply(
    lambda x: 'perforation' if 'perforation' in x.values
    else 'ischemia' if 'ischemia' in x.values
    else 'obstruction' if 'obstruction' in x.values
    else 'inflammation' if 'inflammation' in x.values
    else 'other'
).reset_index()
subtype_by_hadm.columns = ['hadm_id', 'abdomen_subtype']

print(f'Subtype distribution:')
print(subtype_by_hadm['abdomen_subtype'].value_counts().to_string())

# Merge subtype into analysis dataset
stay_vitals_merged = stay_vitals_merged.merge(subtype_by_hadm, on='hadm_id', how='left')
stay_vitals_merged['abdomen_subtype'] = stay_vitals_merged['abdomen_subtype'].fillna('other')

print('\n=== Step 4: Compute Charlson Comorbidity Index ===')

# Simplified CCI based on ICD codes
def compute_cci(diag_df, hadm_ids):
    """Compute Charlson Comorbidity Index from ICD diagnoses"""
    cci_components = {
        'myocardial_infarction': {'icd10': ['I21','I22','I252'], 'icd9': ['410','412'], 'weight': 1},
        'congestive_heart_failure': {'icd10': ['I50','I429'], 'icd9': ['428','39891'], 'weight': 1},
        'peripheral_vascular_disease': {'icd10': ['I70','I71','I73','I771','I790','K551'], 'icd9': ['440','441','443','0930','7854','V434'], 'weight': 1},
        'cerebrovascular_disease': {'icd10': ['I60','I61','I63','I64','I65','I66','I67','I68','I69','G45','G46'], 'icd9': ['430','431','432','433','434','435','436','437','438','36234'], 'weight': 1},
        'dementia': {'icd10': ['F00','F01','F02','F03','G30'], 'icd9': ['290','3310'], 'weight': 1},
        'chronic_pulmonary': {'icd10': ['J40','J41','J42','J43','J44','J45','J46','J47','J60','J61','J62','J63','J64','J65','J66','J67','J684','J701','J703'], 'icd9': ['490','491','492','493','494','495','496','500','501','502','503','504','505','4168','4169','7803'], 'weight': 1},
        'rheumatic_disease': {'icd10': ['M05','M06','M32','M33','M34','M353'], 'icd9': ['7100','7101','7104','7140','7141','7142','7148','725'], 'weight': 1},
        'peptic_ulcer': {'icd10': ['K25','K26','K27','K28'], 'icd9': ['531','532','533','534'], 'weight': 1},
        'liver_disease_mild': {'icd10': ['B18','K700','K701','K702','K703','K709','K713','K714','K715','K717','K719','K740','K741','K742','K743','K744','K745','K746','K762','K763','K764','K769','Z944'], 'icd9': ['070','571','5712','5713','5714','5715','5716','5718','5719','5731','5732','5733','5734','5738','5739','V427'], 'weight': 1},
        'liver_disease_severe': {'icd10': ['K704','K721','K729','K760','K761','K767','K766'], 'icd9': ['5722','5723','5724','5728'], 'weight': 3},
        'diabetes_without_complication': {'icd10': ['E10','E11','E13','E14'], 'icd9': ['250','2500','2501','2502','2503'], 'weight': 1},
        'diabetes_with_complication': {'icd10': ['E102','E103','E104','E105','E107','E112','E113','E114','E115','E117','E132','E133','E134','E135','E137','E142','E143','E144','E145','E147'], 'icd9': ['2504','2505','2506','2507','2508','2509'], 'weight': 2},
        'hemiplegia_paraplegia': {'icd10': ['G81','G82','G83','G041','G114','G801','G802'], 'icd9': ['342','343','3440','3441','3442','3443','3444','3445','3446','3449'], 'weight': 2},
        'renal_disease': {'icd10': ['N18','N19','N052','N053','N054','N055','N056','N057','N250','Z940','Z992','I120','I131'], 'icd9': ['582','583','585','586','588','V420','V451','V56'], 'weight': 2},
        'cancer': {'icd10': ['C00','C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','C22','C23','C24','C25','C26','C30','C31','C32','C33','C34','C37','C38','C39','C40','C41','C43','C45','C46','C47','C48','C49','C50','C51','C52','C53','C54','C55','C56','C57','C58','C60','C61','C62','C63','C64','C65','C66','C67','C68','C69','C70','C71','C72','C73','C74','C75','C76','C77','C78','C79','C80','C81','C82','C83','C84','C85','C86','C88','C90','C91','C92','C93','C94','C95','C96','C97'], 'icd9': ['140','141','142','143','144','145','146','147','148','149','150','151','152','153','154','155','156','157','158','159','160','161','162','163','164','165','166','167','168','169','170','171','172','174','175','176','179','180','181','182','183','184','185','186','187','188','189','190','191','192','193','194','195','196','197','198','199','200','201','202','203','204','205','206','207','208','209','230','231','232','233','234','235','236','237','238','239'], 'weight': 2},
        'metastatic_cancer': {'icd10': ['C77','C78','C79','C80'], 'icd9': ['196','197','198','199'], 'weight': 6},
    }

    diag_filtered = diag_df[diag_df['hadm_id'].isin(hadm_ids)]
    cci_data = []

    for hadm_id in hadm_ids:
        hadm_diag = diag_filtered[diag_filtered['hadm_id'] == hadm_id]
        cci_score = 0
        for component, info in cci_components.items():
            found = False
            for code in hadm_diag['icd_code']:
                code_str = str(code).strip()
                for icd_version in [10, 9]:
                    if hadm_diag[hadm_diag['icd_code']==code]['icd_version'].iloc[0] == icd_version:
                        prefixes = info[f'icd{icd_version}']
                        for prefix in prefixes:
                            if code_str.startswith(prefix):
                                found = True
                                break
            if found:
                cci_score += info['weight']
        cci_data.append({'hadm_id': hadm_id, 'CCI': cci_score})

    return pd.DataFrame(cci_data)

hadm_list = stay_vitals_merged['hadm_id'].unique()
print(f'Computing CCI for {len(hadm_list)} admissions...')
cci_df = compute_cci(diag, hadm_list)
print(f'CCI computed: mean={cci_df["CCI"].mean():.2f}, median={cci_df["CCI"].median():.0f}')

# Merge CCI
stay_vitals_merged = stay_vitals_merged.merge(cci_df, on='hadm_id', how='left')

# Save final dataset
stay_vitals_merged.to_csv(os.path.join(OUT, 'analysis_dataset.csv'), index=False)
print(f'\n=== FINAL DATASET SAVED ===')
print(f'Total stays: {len(stay_vitals_merged)}')
print(f'With SI_first: {stay_vitals_merged["SI_first"].notna().sum()}')
print(f'With MSI_first: {stay_vitals_merged["MSI_first"].notna().sum()}')
print(f'With DSI_first: {stay_vitals_merged["DSI_first"].notna().sum()}')
print(f'With Age_SI_first: {stay_vitals_merged["Age_SI_first"].notna().sum()}')
print(f'ICU death: {stay_vitals_merged["icu_death"].sum()} ({stay_vitals_merged["icu_death"].mean():.3f})')
print(f'Hospital death: {stay_vitals_merged["hospital_death"].sum()} ({stay_vitals_merged["hospital_death"].mean():.3f})')
print(f'Subtype distribution:')
print(stay_vitals_merged['abdomen_subtype'].value_counts().to_string())
print(f'Age: mean={stay_vitals_merged["age_at_admission"].mean():.1f}, median={stay_vitals_merged["age_at_admission"].median():.0f}')
print(f'Gender: {stay_vitals_merged["gender"].value_counts().to_dict()}')
print(f'CCI: mean={stay_vitals_merged["CCI"].mean():.2f}')
