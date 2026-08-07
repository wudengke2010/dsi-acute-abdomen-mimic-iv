"""
eICU Full External Validation for DSI → Acute Abdomen In-Hospital Mortality
============================================================================

Purpose: Apply MIMIC-IV trained Extended+DSI model coefficients to eICU-CRD
         and evaluate discrimination (AUC), calibration (HL P, Brier),
         and incremental value (NRI, IDI).

Strategy:
1. Extract acute abdomen cohort from eICU (same ICD approach as MIMIC-IV)
2. Compute SOFA, DSI, and all extended covariates from eICU tables
3. Apply MIMIC-IV model coefficients (NOT retrain) to predict mortality
4. Evaluate: AUC, DeLong P, calibration, NRI, IDI

Key eICU table mapping:
- patient: demographics, hospital death outcome
- vitalPeriodic: HR, SBP, DBP, MAP (invasive)
- vitalAperiodic: NIBP (non-invasive)
- lab: lactate, WBC, Hb, Cr
- infusionDrug: vasopressors
- respiratoryCare: MV status
- diagnosis: ICD-9 + diagnosis strings for acute abdomen + surgery
- apachePatientResult: APACHE (for SOFA approximation if needed)

Design rule: ALL text boxes, legends, annotations must be placed in
data-empty regions, NEVER obscuring curves/scatter/bar charts.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve, brier_score_loss
import os
import json
import warnings
warnings.filterwarnings('ignore')

EICU_DIR = "E:/mimic-iv/eicu/physionet.org/files/eicu-crd/2.0"
OUTPUT_DIR = "C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen"
PYTHON = "C:/Users/admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe"

print("=" * 70)
print("  eICU Full External Validation: Extended+DSI Model")
print("=" * 70)

# ================================================================
# MIMIC-IV Model Coefficients (from compute_all_stats.py / Table S6)
# These are FIXED — we apply them to eICU without retraining
# ================================================================
# Extended+DSI model (from MIMIC-IV CC N=5728):
# logit(P) = intercept + β1*age_at_admission + β2*sex + β3*CCI + β4*lactate
#           + β5*WBC + β6*vasopressor + β7*surgery + β8*MV
#           + β9*SOFA + β10*DSI_mean_24h

# NOTE: Column names must match cc_analysis DataFrame exactly!
# From Table S6 (verified values):
MODEL_COEFF = {
    'intercept': -3.024,
    'age_at_admission': 0.020,
    'gender_male': 0.145,      # male=1, female=0
    'CCI': 0.101,
    'lactate_first': 0.152,
    'wbc_first': 0.019,
    'vasopressor_use': 0.254,
    'any_surgery': 0.539,
    'mechanical_ventilation': 0.296,
    'sofa': 0.150,             # per point
    'DSI_mean': 0.819,         # DSI=HR/DBP, mean 24h
}

# Extended baseline (no DSI) coefficients:
MODEL_EXT_COEFF = {
    'intercept': -3.387,
    'age_at_admission': 0.022,
    'gender_male': 0.160,
    'CCI': 0.109,
    'lactate_first': 0.167,
    'wbc_first': 0.022,
    'vasopressor_use': 0.317,
    'any_surgery': 0.583,
    'mechanical_ventilation': 0.328,
    'sofa': 0.163,
}

# ── 1. Load eICU patient table ──────────────────────────────────
print("\n[1] Loading eICU patient data...")
patient = pd.read_csv(os.path.join(EICU_DIR, "patient.csv.gz"), compression='gzip',
                       usecols=['patientunitstayid', 'gender', 'age', 'hospitalid',
                                'unittype', 'hospitaladmitsource', 'unitstaytype',
                                'hospitaldischargestatus', 'hospitaldischargeoffset',
                                'admissionweight', 'unitadmitsource',
                                'hospitaladmitoffset'])

# Clean age (eICU has '>89' as string)
patient['age_num'] = patient['age'].replace({'>89': '89', '> 89': '89'}).astype(float)
patient = patient[patient['age_num'] >= 18].copy()
print(f"    Total adult ICU stays: {len(patient):,}")

# Death outcome
patient['mortality'] = (patient['hospitaldischargestatus'] == 'Expired').astype(int)
print(f"    Overall mortality: {patient['mortality'].sum():,} ({patient['mortality'].mean()*100:.1f}%)")

# Gender encoding
patient['gender_male'] = (patient['gender'] == 'Male').astype(int)

# ── 2. Filter acute abdomen ─────────────────────────────────────
print("\n[2] Filtering acute abdomen diagnoses...")
diag = pd.read_csv(os.path.join(EICU_DIR, "diagnosis.csv.gz"), compression='gzip',
                    usecols=['patientunitstayid', 'diagnosisstring', 'icd9code'])

# Same ICD approach as MIMIC-IV paper
# Perforation: K35.0(540.0), K35.1(540.1), K63.1(569.83), K25.1-K25.5(531.1-531.5)
# Ischemia: K55(557), mesenteric ischemia
# Obstruction: K56(560), hernia K44-K46(550-553)
# Inflammation: K35(540), K80(574), K85(577.0), K65(567)
# GI hemorrhage: K92(578)

acute_abd_icd9_prefixes = [
    '540', '541', '542',    # appendicitis/perforation
    '574', '575',           # cholecystitis
    '560',                  # intestinal obstruction
    '567',                  # peritonitis
    '577.0', '577',         # pancreatitis
    '578',                  # GI hemorrhage
    '562',                  # diverticular disease
    '557',                  # vascular/ischemic bowel
    '550', '551', '552', '553',  # hernia (strangulated etc.)
    '531', '532', '533', '534',  # perforated peptic ulcer
    '569.83', '569',       # other perforation
]

acute_abd_keywords = [
    'appendicitis', 'cholecystitis', 'pancreatitis', 'peritonitis',
    'intestinal obstruction', 'bowel obstruction', 'GI hemorrhage',
    'gastrointestinal hemorrhage', 'diverticulitis', 'ischemic bowel',
    'mesenteric ischemia', 'hernia', 'acute abdomen', 'perforated ulcer',
    'perforated bowel', 'strangulated hernia', 'bowel perforation',
]

def is_acute_abd(row):
    icd = str(row['icd9code']) if pd.notna(row['icd9code']) else ''
    diag_str = str(row['diagnosisstring']).lower() if pd.notna(row['diagnosisstring']) else ''
    for prefix in acute_abd_icd9_prefixes:
        if icd.startswith(prefix):
            return True
    for kw in acute_abd_keywords:
        if kw in diag_str:
            return True
    return False

diag['is_acute_abd'] = diag.apply(is_acute_abd, axis=1)
abd_diag = diag[diag['is_acute_abd']].copy()
abd_stay_ids = abd_diag['patientunitstayid'].unique()
abd_patients = patient[patient['patientunitstayid'].isin(abd_stay_ids)].copy()
print(f"    Acute abdomen ICU stays: {len(abd_patients):,}")
print(f"    Mortality: {abd_patients['mortality'].sum():,} ({abd_patients['mortality'].mean()*100:.1f}%)")

# ── 3. Compute Charlson Comorbidity Index ───────────────────────
print("\n[3] Computing CCI from pastHistory...")
pasthist = pd.read_csv(os.path.join(EICU_DIR, "pastHistory.csv.gz"), compression='gzip',
                        usecols=['patientunitstayid', 'pasthistorypath', 'pasthistoryvalue'])

def compute_cci_from_pasthist(stay_id):
    """Compute CCI from eICU pastHistory diagnoses"""
    stay_hist = pasthist[pasthist['patientunitstayid'] == stay_id]
    if len(stay_hist) == 0:
        return 0
    cci = 0
    paths = stay_hist['pasthistorypath'].str.lower().fillna('')
    values = stay_hist['pasthistoryvalue'].str.lower().fillna('')

    all_text = ' '.join(paths) + ' '.join(values)

    # CCI components (simplified mapping)
    if 'myocardial infarct' in all_text: cci += 1
    if 'congestive heart failure' in all_text or 'chf' in all_text: cci += 1
    if 'peripheral vascular' in all_text or 'pvd' in all_text: cci += 1
    if 'cerebrovascular' in all_text or 'cvd' in all_text or 'stroke' in all_text: cci += 1
    if 'dementia' in all_text: cci += 1
    if 'chronic pulmonary' in all_text or 'copd' in all_text: cci += 1
    if 'rheumatoid' in all_text or 'connective tissue' in all_text: cci += 1
    if 'peptic ulcer' in all_text: cci += 1
    if 'diabetes' in all_text:
        if 'complication' in all_text or 'end organ' in all_text:
            cci += 2
        else:
            cci += 1
    if 'hemiplegia' in all_text or 'paraplegia' in all_text: cci += 2
    if 'renal' in all_text or 'kidney disease' in all_text: cci += 2
    if 'malignancy' in all_text or 'cancer' in all_text or 'lymphoma' in all_text:
        if 'metastatic' in all_text or 'metastasis' in all_text:
            cci += 6
        else:
            cci += 2
    if 'leukemia' in all_text: cci += 2
    if 'liver' in all_text or 'hepatic' in all_text:
        if 'severe' in all_text:
            cci += 3
        else:
            cci += 1
    return cci

# Apply CCI computation (batch approach for speed)
print("    Computing CCI for all acute abdomen patients...")
cci_map = {}
for sid in abd_patients['patientunitstayid'].values:
    cci_map[sid] = compute_cci_from_pasthist(sid)
abd_patients['CCI'] = abd_patients['patientunitstayid'].map(cci_map)
print(f"    CCI: median={abd_patients['CCI'].median()}, IQR={abd_patients['CCI'].quantile(0.25)}-{abd_patients['CCI'].quantile(0.75)}")

# ── 4. Extract vital signs → SI/MSI/DSI/Age-SI (mean 24h) ──────
print("\n[4] Extracting vital signs (24h mean)...")
chunksize = 500000
vitals_list = []

for chunk in pd.read_csv(os.path.join(EICU_DIR, "vitalPeriodic.csv.gz"), compression='gzip',
                          usecols=['patientunitstayid', 'observationoffset',
                                   'heartrate', 'systemicsystolic',
                                   'systemicdiastolic', 'systemicmean'],
                          chunksize=chunksize):
    filtered = chunk[chunk['patientunitstayid'].isin(abd_stay_ids)]
    # Filter to first 24h (1440 minutes)
    filtered = filtered[(filtered['observationoffset'] >= 0) &
                        (filtered['observationoffset'] <= 1440)]
    if len(filtered) > 0:
        vitals_list.append(filtered)

vitals = pd.concat(vitals_list, ignore_index=True)
print(f"    Vital records (24h): {len(vitals):,}")

# Also load vitalAperiodic for NIBP (non-invasive BP) as fallback
print("    Loading NIBP data (vitalAperiodic)...")
vitals_aper_list = []
for chunk in pd.read_csv(os.path.join(EICU_DIR, "vitalAperiodic.csv.gz"), compression='gzip',
                          usecols=['patientunitstayid', 'observationoffset',
                                   'noninvasivesystolic', 'noninvasivediastolic', 'noninvasivemean'],
                          chunksize=chunksize):
    filtered = chunk[chunk['patientunitstayid'].isin(abd_stay_ids)]
    filtered = filtered[(filtered['observationoffset'] >= 0) &
                        (filtered['observationoffset'] <= 1440)]
    if len(filtered) > 0:
        vitals_aper_list.append(filtered)

vitals_aper = pd.concat(vitals_aper_list, ignore_index=True) if vitals_aper_list else pd.DataFrame()
print(f"    NIBP records (24h): {len(vitals_aper):,}")

# BP priority: invasive > NIBP (same as MIMIC-IV paper)
# Compute mean 24h values per stay
inv_mean = vitals.groupby('patientunitstayid').agg(
    HR_mean=('heartrate', 'mean'),
    SBP_inv_mean=('systemicsystolic', 'mean'),
    DBP_inv_mean=('systemicdiastolic', 'mean'),
    MAP_inv_mean=('systemicmean', 'mean'),
    HR_count=('heartrate', 'count'),
    SBP_inv_count=('systemicsystolic', 'count'),
).reset_index()

# NIBP mean
if len(vitals_aper) > 0:
    nibp_mean = vitals_aper.groupby('patientunitstayid').agg(
        SBP_nibp_mean=('noninvasivesystolic', 'mean'),
        DBP_nibp_mean=('noninvasivediastolic', 'mean'),
        MAP_nibp_mean=('noninvasivemean', 'mean'),
        SBP_nibp_count=('noninvasivesystolic', 'count'),
    ).reset_index()
else:
    nibp_mean = pd.DataFrame(columns=['patientunitstayid', 'SBP_nibp_mean', 'DBP_nibp_mean',
                                      'MAP_nibp_mean', 'SBP_nibp_count'])

# Merge: priority invasive > NIBP
bp_merged = inv_mean.merge(nibp_mean, on='patientunitstayid', how='outer')

# Apply priority: if invasive SBP available, use it; else NIBP
bp_merged['SBP_mean'] = bp_merged['SBP_inv_mean'].fillna(bp_merged['SBP_nibp_mean'])
bp_merged['DBP_mean'] = bp_merged['DBP_inv_mean'].fillna(bp_merged['DBP_nibp_mean'])
bp_merged['MAP_mean'] = bp_merged['MAP_inv_mean'].fillna(bp_merged['MAP_nibp_mean'])

# Compute SI derivatives
bp_merged['SI_mean'] = bp_merged['HR_mean'] / bp_merged['SBP_mean']
bp_merged['MSI_mean'] = bp_merged['HR_mean'] / bp_merged['MAP_mean']
bp_merged['DSI_mean'] = bp_merged['HR_mean'] / bp_merged['DBP_mean']
bp_merged['Age_SI_mean'] = bp_merged['SI_mean'] * bp_merged['HR_mean']  # placeholder; need age

# Merge with patient age
bp_merged = bp_merged.merge(
    abd_patients[['patientunitstayid', 'age_num', 'mortality', 'gender_male', 'CCI']],
    on='patientunitstayid', how='inner'
)

# Fix Age_SI = SI × Age/10
bp_merged['Age_SI_mean'] = bp_merged['SI_mean'] * bp_merged['age_num'] / 10

# Remove physiologically impossible values
bp_merged = bp_merged[
    (bp_merged['HR_mean'] > 20) & (bp_merged['HR_mean'] < 300) &
    (bp_merged['SBP_mean'] > 30) & (bp_merged['SBP_mean'] < 300) &
    (bp_merged['DBP_mean'] > 10) & (bp_merged['DBP_mean'] < 200) &
    (bp_merged['SI_mean'] > 0) & (bp_merged['SI_mean'] < 5) &
    (bp_merged['DSI_mean'] > 0) & (bp_merged['DSI_mean'] < 10) &
    (bp_merged['MSI_mean'] > 0) & (bp_merged['MSI_mean'] < 5)
].copy()

print(f"    Cohort with complete vitals: {len(bp_merged):,}")
print(f"    Mortality: {bp_merged['mortality'].sum():,} ({bp_merged['mortality'].mean()*100:.1f}%)")

# ── 5. Extract laboratory values ────────────────────────────────
print("\n[5] Extracting laboratory values (first 24h)...")
lab_names = ['lactate', 'WBC x 1000', 'Hemoglobin', 'creatinine']

lab_list = []
for chunk in pd.read_csv(os.path.join(EICU_DIR, "lab.csv.gz"), compression='gzip',
                          usecols=['patientunitstayid', 'labresultoffset',
                                   'labname', 'labresult'],
                          chunksize=chunksize):
    filtered = chunk[chunk['patientunitstayid'].isin(abd_stay_ids)]
    filtered = filtered[
        (filtered['labname'].isin(lab_names)) &
        (filtered['labresultoffset'] >= 0) &
        (filtered['labresultoffset'] <= 1440) &
        (filtered['labresult'].notna())
    ]
    if len(filtered) > 0:
        lab_list.append(filtered)

lab_df = pd.concat(lab_list, ignore_index=True) if lab_list else pd.DataFrame()
print(f"    Lab records: {len(lab_df):,}")

# Take first value per stay per lab
if len(lab_df) > 0:
    lab_first = lab_df.groupby(['patientunitstayid', 'labname']).agg(
        first_value=('labresult', 'first'),
    ).reset_index()

    # Pivot to wide format — dynamic column names
    lab_wide = lab_first.pivot(index='patientunitstayid', columns='labname',
                               values='first_value').reset_index()
    # Rename columns to match MIMIC-IV naming
    col_rename = {}
    for col in lab_wide.columns:
        if col == 'patientunitstayid': continue
        if 'lactate' in col.lower(): col_rename[col] = 'lactate_first'
        elif 'wbc' in col.lower(): col_rename[col] = 'wbc_first'
        elif 'hemoglobin' in col.lower() or 'hb' in col.lower(): col_rename[col] = 'hb_first'
        elif 'creatinine' in col.lower() or 'cr' in col.lower(): col_rename[col] = 'cr_first'
        else: col_rename[col] = col
    lab_wide.rename(columns=col_rename, inplace=True)
else:
    lab_wide = pd.DataFrame(columns=['patientunitstayid', 'lactate_first',
                                      'wbc_first', 'hb_first', 'cr_first'])

print(f"    Lactate coverage: {lab_wide['lactate_first'].notna().sum()}/{len(bp_merged)}")
print(f"    WBC coverage: {lab_wide['wbc_first'].notna().sum()}/{len(bp_merged)}")

# ── 6. Extract vasopressor use ──────────────────────────────────
print("\n[6] Extracting vasopressor use (24h)...")
vasopressor_names = ['norepinephrine', 'vasopressin', 'dopamine',
                     'epinephrine', 'phenylephrine', 'dobutamine',
                     'milrinone', 'levophed', 'neosynephrine']

vaso_list = []
for chunk in pd.read_csv(os.path.join(EICU_DIR, "infusionDrug.csv.gz"), compression='gzip',
                          usecols=['patientunitstayid', 'infusionoffset',
                                   'drugname', 'drugrate'],
                          chunksize=chunksize):
    filtered = chunk[chunk['patientunitstayid'].isin(abd_stay_ids)]
    # Within first 24h
    filtered = filtered[(filtered['infusionoffset'] >= 0) &
                        (filtered['infusionoffset'] <= 1440)]
    # Check vasopressor names
    filtered['is_vaso'] = filtered['drugname'].str.lower().apply(
        lambda x: any(vn in str(x) for vn in vasopressor_names) if pd.notna(x) else False
    )
    vaso_found = filtered[filtered['is_vaso']]
    if len(vaso_found) > 0:
        vaso_list.append(vaso_found[['patientunitstayid']].drop_duplicates())

if vaso_list:
    vaso_patients = pd.concat(vaso_list).drop_duplicates()
    vaso_patients['vasopressor_use'] = 1
    print(f"    Vasopressor patients: {len(vaso_patients):,}")
else:
    vaso_patients = pd.DataFrame(columns=['patientunitstayid', 'vasopressor_use'])
    print("    No vasopressor patients found")

# ── 7. Extract mechanical ventilation ────────────────────────────
print("\n[7] Extracting mechanical ventilation status...")
# Use respiratoryCare table: ventstartoffset indicates MV
resp_list = []
for chunk in pd.read_csv(os.path.join(EICU_DIR, "respiratoryCare.csv.gz"), compression='gzip',
                          usecols=['patientunitstayid', 'ventstartoffset'],
                          chunksize=chunksize):
    filtered = chunk[chunk['patientunitstayid'].isin(abd_stay_ids)]
    # MV started within first 24h
    filtered = filtered[(filtered['ventstartoffset'] >= 0) &
                        (filtered['ventstartoffset'] <= 1440) &
                        (filtered['ventstartoffset'].notna())]
    if len(filtered) > 0:
        resp_list.append(filtered[['patientunitstayid']].drop_duplicates())

if resp_list:
    mv_patients = pd.concat(resp_list).drop_duplicates()
    mv_patients['mechanical_ventilation'] = 1
    print(f"    MV patients: {len(mv_patients):,}")
else:
    mv_patients = pd.DataFrame(columns=['patientunitstayid', 'mechanical_ventilation'])
    print("    No MV patients found")

# ── 8. Determine surgery status ──────────────────────────────────
print("\n[8] Determining surgery status from treatment/diagnosis...")
# Surgery in eICU is harder to determine; use treatment table + admissionDx
treat_list = []
for chunk in pd.read_csv(os.path.join(EICU_DIR, "treatment.csv.gz"), compression='gzip',
                          usecols=['patientunitstayid', 'treatmentoffset',
                                   'treatmentstring'],
                          chunksize=chunksize):
    filtered = chunk[chunk['patientunitstayid'].isin(abd_stay_ids)]
    filtered = filtered[(filtered['treatmentoffset'] >= 0) &
                        (filtered['treatmentoffset'] <= 1440)]
    filtered['is_surgery'] = filtered['treatmentstring'].str.lower().apply(
        lambda x: any(kw in str(x) for kw in ['surgery', 'operative', 'laparotomy',
                                                'appendectomy', 'cholecystectomy',
                                                'bowel resection', 'repair',
                                                'laparoscopy', 'procedure']) if pd.notna(x) else False
    )
    surg_found = filtered[filtered['is_surgery']]
    if len(surg_found) > 0:
        treat_list.append(surg_found[['patientunitstayid']].drop_duplicates())

if treat_list:
    surg_patients = pd.concat(treat_list).drop_duplicates()
    surg_patients['any_surgery'] = 1
    print(f"    Surgery patients (within 24h): {len(surg_patients):,}")
else:
    surg_patients = pd.DataFrame(columns=['patientunitstayid', 'any_surgery'])
    print("    No surgery patients found")

# ── 9. Compute SOFA score ────────────────────────────────────────
print("\n[9] Computing SOFA score from eICU data...")
# SOFA = Respiration + Coagulation + Liver + Cardiovascular + CNS + Renal
# We approximate from available eICU data

# Use APACHE as surrogate for SOFA if available
# Or compute from components

# Simplified SOFA computation:
# Respiratory: PaO2/FiO2 → use SpO2/FiO2 proxy or ventilator status
# Cardiovascular: vasopressor + MAP → already extracted
# CNS: GCS → available in physicalExam
# Renal: creatinine → from lab
# Liver: bilirubin → from lab (if available)
# Coagulation: platelets → from lab (if available)

# For pragmatic approach: use apacheApsVar (APS components correlate with SOFA)
print("    Using APACHE APS variables for SOFA computation...")

apache_aps = pd.read_csv(os.path.join(EICU_DIR, "apacheApsVar.csv.gz"), compression='gzip',
                          usecols=['apacheapsvarid', 'patientunitstayid',
                                   'eyes', 'motor', 'verbal',  # GCS components
                                   'creatinine', 'bilirubin',
                                   'wbc', 'urine', 'sodium',
                                   'temperature', 'heartrate', 'meanbp',
                                   'respiratoryrate', 'pao2', 'fio2',
                                   'ph', 'albumin', 'intubated', 'vent',
                                   'hematocrit', 'bun', 'glucose', 'pco2'])

# GCS
apache_aps['gcs'] = apache_aps['eyes'].fillna(0) + apache_aps['motor'].fillna(0) + apache_aps['verbal'].fillna(0)
apache_aps['gcs'] = apache_aps['gcs'].replace(0, 15)  # 0 often means unmeasured = normal

# Compute SOFA components
# Respiratory: if on ventilator → assume 2+ if PaO2 available
# Cardiovascular: based on vasopressor + MAP
# CNS: based on GCS
# Renal: based on creatinine
# Liver: based on bilirubin (if available)
# Coagulation: based on platelets (if available)

def compute_sofa_row(row, vaso_dict, mv_dict):
    sofa = 0

    # Respiration (0-4)
    if row.get('pao2', None) is not None and pd.notna(row.get('pao2')):
        fio2 = row.get('fio2', 0.21) if pd.notna(row.get('fio2')) else 0.21
        if fio2 < 0.21: fio2 = 0.21
        pf_ratio = row['pao2'] / fio2
        if pf_ratio < 100: sofa += 4
        elif pf_ratio < 200: sofa += 3
        elif pf_ratio < 300: sofa += 2
        elif pf_ratio < 400: sofa += 1
        else: sofa += 0
    elif mv_dict.get(row['patientunitstayid'], 0) == 1:
        sofa += 2  # MV without PaO2 data → assume moderate

    # Coagulation (0-4) - hematocrit proxy (eICU lacks platelets in APS)
    # Use hematocrit: normal ~40%, <30% suggests thrombocytopenia
    if pd.notna(row.get('hematocrit')):
        hct = row['hematocrit']
        # Rough proxy: Hct<20 → likely platelets<20 (score 4)
        if hct < 20: sofa += 4
        elif hct < 25: sofa += 2  # moderate coagulopathy
        elif hct < 30: sofa += 1  # mild

    # Liver (0-4) - bilirubin
    if pd.notna(row.get('bilirubin')):
        bili = row['bilirubin']
        if bili >= 12: sofa += 4
        elif bili >= 6: sofa += 3
        elif bili >= 2: sofa += 2
        elif bili >= 1.2: sofa += 1

    # Cardiovascular (0-4) - vasopressor + MAP
    if vaso_dict.get(row['patientunitstayid'], 0) == 1:
        # Has vasopressor → at least 3-4
        map_val = row.get('meanbp', 70)
        if pd.notna(map_val) and map_val < 70:
            sofa += 4  # vasopressor + MAP<70
        else:
            sofa += 3  # vasopressor + MAP≥70
    else:
        map_val = row.get('meanbp', 80)
        if pd.notna(map_val) and map_val < 70:
            sofa += 1  # MAP<70 without vasopressor

    # CNS (0-4) - GCS
    gcs = row.get('gcs', 15)
    if gcs < 6: sofa += 4
    elif gcs < 9: sofa += 3
    elif gcs < 13: sofa += 2
    elif gcs < 15: sofa += 1

    # Renal (0-4) - creatinine
    if pd.notna(row.get('creatinine')):
        cr = row['creatinine']
        if cr >= 5: sofa += 4
        elif cr >= 3.5: sofa += 3
        elif cr >= 2: sofa += 2
        elif cr >= 1.2: sofa += 1

    return sofa

# Prepare dictionaries for fast lookup
vaso_dict = dict(zip(vaso_patients['patientunitstayid'], vaso_patients['vasopressor_use']))
mv_dict = dict(zip(mv_patients['patientunitstayid'], mv_patients['mechanical_ventilation']))

# Compute SOFA for each patient
# Filter apache_aps to our cohort
apache_cohort = apache_aps[apache_aps['patientunitstayid'].isin(abd_stay_ids)].copy()
# Take first APS record per stay
apache_first = apache_cohort.groupby('patientunitstayid').first().reset_index()

print(f"    APACHE APS records for cohort: {len(apache_first):,}")

sofa_values = []
for _, row in apache_first.iterrows():
    sofa_values.append(compute_sofa_row(row, vaso_dict, mv_dict))

apache_first['sofa'] = sofa_values
print(f"    SOFA: median={apache_first['sofa'].median()}, IQR={apache_first['sofa'].quantile(0.25)}-{apache_first['sofa'].quantile(0.75)}")

# ── 10. Build complete analysis dataset ──────────────────────────
print("\n[10] Building complete analysis dataset...")

# Merge all data
analysis = bp_merged[['patientunitstayid', 'age_num', 'gender_male', 'CCI',
                       'mortality', 'SI_mean', 'MSI_mean', 'DSI_mean',
                       'Age_SI_mean', 'HR_mean', 'SBP_mean', 'DBP_mean']].copy()

# Add labs
analysis = analysis.merge(lab_wide, on='patientunitstayid', how='left')

# Add vasopressor
analysis = analysis.merge(vaso_patients, on='patientunitstayid', how='left')
analysis['vasopressor_use'] = analysis['vasopressor_use'].fillna(0).astype(int)

# Add MV
analysis = analysis.merge(mv_patients, on='patientunitstayid', how='left')
analysis['mechanical_ventilation'] = analysis['mechanical_ventilation'].fillna(0).astype(int)

# Add surgery
analysis = analysis.merge(surg_patients, on='patientunitstayid', how='left')
analysis['any_surgery'] = analysis['any_surgery'].fillna(0).astype(int)

# Add SOFA
analysis = analysis.merge(apache_first[['patientunitstayid', 'sofa']],
                          on='patientunitstayid', how='left')
# Fill missing SOFA with median
analysis['sofa'] = analysis['sofa'].fillna(apache_first['sofa'].median())

# Rename age_num to age_at_admission for consistency
analysis.rename(columns={'age_num': 'age_at_admission'}, inplace=True)

# Complete case: require DSI + at least lactate (like MIMIC-IV CC)
cc_analysis = analysis.dropna(subset=['DSI_mean', 'lactate_first']).copy()
print(f"    Complete case cohort (DSI+lactate): {len(cc_analysis):,}")
print(f"    CC mortality: {cc_analysis['mortality'].sum():,} ({cc_analysis['mortality'].mean()*100:.1f}%)")
print(f"    CC age: median={cc_analysis['age_at_admission'].median()}")
print(f"    CC DSI: median={cc_analysis['DSI_mean'].median():.3f}")
print(f"    CC SOFA: median={cc_analysis['sofa'].median()}")

# ── 11. Apply MIMIC-IV model coefficients ────────────────────────
print("\n[11] Applying MIMIC-IV trained model to eICU data...")

def predict_with_coeff(df, coeff_dict):
    """Apply fixed model coefficients to compute linear predictor (logit)"""
    logit = coeff_dict['intercept']
    matched_vars = []
    unmatched_vars = []
    for var, beta in coeff_dict.items():
        if var == 'intercept':
            continue
        if var in df.columns:
            logit += beta * df[var]
            matched_vars.append(var)
        else:
            unmatched_vars.append(var)
    print(f"    Matched variables: {matched_vars}")
    if unmatched_vars:
        print(f"    WARNING: Unmatched variables: {unmatched_vars}")
    return logit  # Return logit for recalibration flexibility

# Fill remaining missing values with median (for model prediction)
# In external validation, median imputation from training data is recommended
fill_cols = ['lactate_first', 'wbc_first', 'hb_first', 'cr_first',
             'vasopressor_use', 'mechanical_ventilation', 'any_surgery', 'sofa']
for col in fill_cols:
    if col in cc_analysis.columns and cc_analysis[col].isna().any():
        median_val = cc_analysis[col].median()
        n_missing = cc_analysis[col].isna().sum()
        cc_analysis[col] = cc_analysis[col].fillna(median_val)
        print(f"    Filled {col} NaN with median={median_val:.2f} ({n_missing} filled)")

# Compute raw logits
print("    Computing Extended baseline logit...")
logit_ext = predict_with_coeff(cc_analysis, MODEL_EXT_COEFF)
print("    Computing Extended+DSI logit...")
logit_ext_dsi = predict_with_coeff(cc_analysis, MODEL_COEFF)

# Raw probabilities (for initial AUC only)
p_ext_raw = 1 / (1 + np.exp(-logit_ext))
p_ext_dsi_raw = 1 / (1 + np.exp(-logit_ext_dsi))

# Verify no NaN
assert not np.any(np.isnan(p_ext_raw)), "NaN in Extended predictions!"
assert not np.any(np.isnan(p_ext_dsi_raw)), "NaN in Extended+DSI predictions!"

# ── 11b. Logistic recalibration ──────────────────────────────────
print("\n[11b] Logistic recalibration (intercept+slope adjustment)...")
# In external validation, recalibration by fitting: logit(P) = a + b * linear_predictor
# This adjusts the intercept and slope to the external dataset
# Per TRIPOD: report both original and recalibrated performance

y = cc_analysis['mortality'].values

def logistic_recalibrate(y_true, logit_pred):
    """Logistic recalibration: fit new intercept and slope on external data"""
    from sklearn.linear_model import LogisticRegression
    X = logit_pred.values.reshape(-1, 1)
    lr = LogisticRegression(C=1e6, solver='lbfgs', max_iter=1000)
    lr.fit(X, y_true)
    a = lr.intercept_[0]
    b = lr.coef_[0][0]
    p_recal = lr.predict_proba(X)[:, 1]
    return p_recal, a, b

# Recalibrate Extended baseline
p_ext_recal, a_ext, b_ext = logistic_recalibrate(y, logit_ext)
print(f"    Extended recal: intercept_shift={a_ext:.3f}, slope={b_ext:.3f}")

# Recalibrate Extended+DSI
p_ext_dsi_recal, a_dsi, b_dsi = logistic_recalibrate(y, logit_ext_dsi)
print(f"    Ext+DSI recal: intercept_shift={a_dsi:.3f}, slope={b_dsi:.3f}")

# Evaluate AUC (AUC is rank-based, doesn't change with recalibration)
auc_ext = roc_auc_score(y, p_ext_raw)
auc_ext_dsi = roc_auc_score(y, p_ext_dsi_raw)
delta_auc = auc_ext_dsi - auc_ext

print(f"\n    === eICU External Validation Results ===")
print(f"    Extended baseline AUC: {auc_ext:.3f}")
print(f"    Extended+DSI AUC:      {auc_ext_dsi:.3f}")
print(f"    ΔAUC:                  {delta_auc:.4f}")
print(f"    MIMIC-IV comparison:")
print(f"      MIMIC Ext AUC:    0.787")
print(f"      MIMIC Ext+DSI:    0.792")
print(f"      MIMIC ΔAUC:       0.005")

# ── 12. DeLong test for AUC comparison ──────────────────────────
print("\n[12] DeLong test for ΔAUC significance...")

# DeLong test implementation (placement value method)
def delong_test(y_true, y_pred1, y_pred2):
    """Compute DeLong z-test for two correlated AUCs"""
    n1 = np.sum(y_true == 1)
    n0 = np.sum(y_true == 0)

    pred1_pos = y_pred1[y_true == 1]
    pred1_neg = y_pred1[y_true == 0]
    pred2_pos = y_pred2[y_true == 1]
    pred2_neg = y_pred2[y_true == 0]

    # Placement values
    V10_1 = np.array([np.mean(pred1_neg < p) + 0.5*np.mean(pred1_neg == p) for p in pred1_pos])
    V01_1 = np.array([np.mean(pred1_pos > p) + 0.5*np.mean(pred1_pos == p) for p in pred1_neg])
    V10_2 = np.array([np.mean(pred2_neg < p) + 0.5*np.mean(pred2_neg == p) for p in pred2_pos])
    V01_2 = np.array([np.mean(pred2_pos > p) + 0.5*np.mean(pred2_pos == p) for p in pred2_neg])

    # Covariance matrices
    S10 = np.cov(np.vstack([V10_1, V10_2]), bias=True)
    S01 = np.cov(np.vstack([V01_1, V01_2]), bias=True)

    var_auc1 = S10[0, 0] / n1 + S01[0, 0] / n0
    var_auc2 = S10[1, 1] / n1 + S01[1, 1] / n0
    cov_auc = S10[0, 1] / n1 + S01[0, 1] / n0

    var_diff = var_auc1 + var_auc2 - 2 * cov_auc
    z = (auc_ext_dsi - auc_ext) / np.sqrt(max(var_diff, 1e-10))
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return z, p_value

z_delong, p_delong = delong_test(y, p_ext_raw, p_ext_dsi_raw)
print(f"    DeLong z = {z_delong:.3f}, P = {p_delong:.4f}")

# ── 13. Calibration ─────────────────────────────────────────────
print("\n[13] Calibration assessment (before and after recalibration)...")

# Hosmer-Lemeshow test
def hosmer_lemeshow_test(y_true, y_pred, n_groups=10):
    """Hosmer-Lemeshow chi-squared test"""
    pred_series = pd.Series(y_pred)
    deciles = pd.qcut(pred_series, n_groups, duplicates='drop')

    obs = pd.Series(y_true).groupby(deciles).sum()
    exp = pred_series.groupby(deciles).sum()
    n = pd.Series(y_true).groupby(deciles).count()

    hl_chi2 = 0
    for i in range(len(obs)):
        o = obs.iloc[i]
        e = exp.iloc[i]
        n_i = n.iloc[i]
        if e > 0:
            hl_chi2 += (o - e)**2 / e
        if (n_i - e) > 0:
            hl_chi2 += ((n_i - o) - (n_i - e))**2 / (n_i - e)

    df = len(obs) - 2
    p_value = 1 - stats.chi2.cdf(hl_chi2, df)
    return hl_chi2, df, p_value

# Before recalibration
brier_ext_raw = brier_score_loss(y, p_ext_raw)
brier_ext_dsi_raw = brier_score_loss(y, p_ext_dsi_raw)
hl_chi2_ext_raw, hl_df_ext_raw, hl_p_ext_raw = hosmer_lemeshow_test(y, p_ext_raw)
hl_chi2_dsi_raw, hl_df_dsi_raw, hl_p_dsi_raw = hosmer_lemeshow_test(y, p_ext_dsi_raw)

print(f"    BEFORE recalibration:")
print(f"      Extended: Brier={brier_ext_raw:.4f}, HL P={hl_p_ext_raw:.3f}")
print(f"      Ext+DSI:  Brier={brier_ext_dsi_raw:.4f}, HL P={hl_p_dsi_raw:.3f}")

# After recalibration (this is the proper way to evaluate calibration in external validation)
brier_ext_recal = brier_score_loss(y, p_ext_recal)
brier_ext_dsi_recal = brier_score_loss(y, p_ext_dsi_recal)
hl_chi2_ext_recal, hl_df_ext_recal, hl_p_ext_recal = hosmer_lemeshow_test(y, p_ext_recal)
hl_chi2_dsi_recal, hl_df_dsi_recal, hl_p_dsi_recal = hosmer_lemeshow_test(y, p_ext_dsi_recal)

print(f"    AFTER logistic recalibration:")
print(f"      Extended: Brier={brier_ext_recal:.4f}, HL P={hl_p_ext_recal:.3f}")
print(f"      Ext+DSI:  Brier={brier_ext_dsi_recal:.4f}, HL P={hl_p_dsi_recal:.3f}")

# ── 14. NRI and IDI ──────────────────────────────────────────────
print("\n[14] Computing NRI and IDI (using recalibrated predictions)...")

def compute_nri_idi(y_true, p_old, p_new):
    """Compute category-free NRI and IDI with proper SE estimation"""
    events = y_true == 1
    nonevents = y_true == 0
    n_e = np.sum(events)
    n_ne = np.sum(nonevents)

    # IDI = (IS_new - IS_old for events) - (IS_new - IS_old for nonevents)
    # IS = integrated sensitivity = mean predicted probability for events
    IS_new_e = np.mean(p_new[events])
    IS_old_e = np.mean(p_old[events])
    IS_new_ne = np.mean(p_new[nonevents])
    IS_old_ne = np.mean(p_old[nonevents])
    
    idi = (IS_new_e - IS_old_e) - (IS_new_ne - IS_old_ne)
    
    # SE for IDI (per Pencina 2008)
    se_idi_e = np.std(p_new[events] - p_old[events]) / np.sqrt(n_e)
    se_idi_ne = np.std(p_new[nonevents] - p_old[nonevents]) / np.sqrt(n_ne)
    idi_se = np.sqrt(se_idi_e**2 + se_idi_ne**2)
    idi_z = idi / idi_se
    idi_p = 2 * (1 - stats.norm.cdf(abs(idi_z)))

    # Category-free NRI (continuous NRI)
    delta_e = p_new[events] - p_old[events]
    delta_ne = p_new[nonevents] - p_old[nonevents]
    
    # For events: upward risk movement is GOOD, downward is BAD
    nri_e = np.sum(delta_e > 0) / n_e - np.sum(delta_e < 0) / n_e
    # For nonevents: downward risk movement is GOOD, upward is BAD
    nri_ne = np.sum(delta_ne < 0) / n_ne - np.sum(delta_ne > 0) / n_ne
    nri_cf = nri_e + nri_ne
    
    # SE for category-free NRI (per Pencina 2008)
    se_nri_e = np.sqrt(np.var(delta_e > 0)/n_e + np.var(delta_e < 0)/n_e)
    se_nri_ne = np.sqrt(np.var(delta_ne < 0)/n_ne + np.var(delta_ne > 0)/n_ne)
    nri_se = np.sqrt(se_nri_e**2 + se_nri_ne**2)
    nri_z = nri_cf / max(nri_se, 1e-10)
    nri_p = 2 * (1 - stats.norm.cdf(abs(nri_z)))

    return {
        'nri_cf': nri_cf, 'nri_cf_se': nri_se, 'nri_cf_p': nri_p,
        'nri_e': nri_e, 'nri_ne': nri_ne,
        'idi': idi, 'idi_se': idi_se, 'idi_p': idi_p,
    }

# Use recalibrated predictions for NRI/IDI (calibration-adjusted)
nri_idi = compute_nri_idi(y, p_ext_recal, p_ext_dsi_recal)
print(f"    Category-free NRI: {nri_idi['nri_cf']:.3f} (SE={nri_idi['nri_cf_se']:.3f}, P={nri_idi['nri_cf_p']:.4f})")
print(f"    NRI_events: {nri_idi['nri_e']:.3f}, NRI_nonevents: {nri_idi['nri_ne']:.3f}")
print(f"    IDI: {nri_idi['idi']:.3f} (SE={nri_idi['idi_se']:.3f}, P={nri_idi['idi_p']:.4f})")

# ── 15. DSI quartile analysis ────────────────────────────────────
print("\n[15] DSI quartile mortality gradient in eICU...")
# Use MIMIC-IV cutoffs for external validation (as recommended by TRIPOD)
dsi_q_cutoffs = [1.279, 1.502, 1.762]  # From MIMIC-IV
cc_analysis['dsi_quartile'] = pd.cut(cc_analysis['DSI_mean'],
                                      bins=[0, 1.279, 1.502, 1.762, float('inf')],
                                      labels=['Q1', 'Q2', 'Q3', 'Q4'])

for q in ['Q1', 'Q2', 'Q3', 'Q4']:
    n = len(cc_analysis[cc_analysis['dsi_quartile'] == q])
    deaths = cc_analysis[cc_analysis['dsi_quartile'] == q]['mortality'].sum()
    rate = deaths / n * 100 if n > 0 else 0
    print(f"    {q}: N={n:,}, deaths={deaths}, mortality={rate:.1f}%")

# ── 16. Save results ─────────────────────────────────────────────
print("\n[16] Saving results...")

results = {
    'cohort': {
        'total_abd_stays': len(abd_patients),
        'cc_n': len(cc_analysis),
        'cc_mortality_pct': round(cc_analysis['mortality'].mean()*100, 1),
        'cc_mortality_n': int(cc_analysis['mortality'].sum()),
        'cc_age_median': float(cc_analysis['age_at_admission'].median()),
        'cc_age_iqr': [float(cc_analysis['age_at_admission'].quantile(0.25)),
                       float(cc_analysis['age_at_admission'].quantile(0.75))],
        'cc_male_pct': round(cc_analysis['gender_male'].mean()*100, 1),
        'cc_sofa_median': float(cc_analysis['sofa'].median()),
        'cc_sofa_iqr': [float(cc_analysis['sofa'].quantile(0.25)),
                        float(cc_analysis['sofa'].quantile(0.75))],
        'cc_dsi_median': round(float(cc_analysis['DSI_mean'].median()), 3),
        'cc_lactate_coverage_pct': round(cc_analysis['lactate_first'].notna().mean()*100, 1),
        'mimic_iv_comparison': {
            'mimic_cc_n': 5728,
            'mimic_mortality_pct': 19.9,
            'mimic_sofa_median': 7,
        }
    },
    'auc': {
        'extended': round(auc_ext, 3),
        'extended_dsi': round(auc_ext_dsi, 3),
        'delta_auc': round(delta_auc, 4),
        'delong_z': round(z_delong, 3),
        'delong_p': round(p_delong, 4),
        'mimic_iv_comparison': {
            'mimic_ext_auc': 0.787,
            'mimic_ext_dsi_auc': 0.792,
            'mimic_delta_auc': 0.005,
            'mimic_delong_p': 0.012,
        }
    },
    'calibration_raw': {
        'extended_brier': round(brier_ext_raw, 4),
        'extended_hl_p': round(hl_p_ext_raw, 3),
        'extended_dsi_brier': round(brier_ext_dsi_raw, 4),
        'extended_dsi_hl_p': round(hl_p_dsi_raw, 3),
    },
    'calibration_recalibrated': {
        'extended_brier': round(brier_ext_recal, 4),
        'extended_hl_p': round(hl_p_ext_recal, 3),
        'extended_dsi_brier': round(brier_ext_dsi_recal, 4),
        'extended_dsi_hl_p': round(hl_p_dsi_recal, 3),
        'recal_intercept_shift_ext': round(a_ext, 3),
        'recal_slope_ext': round(b_ext, 3),
        'recal_intercept_shift_dsi': round(a_dsi, 3),
        'recal_slope_dsi': round(b_dsi, 3),
    },
    'nri_idi': {
        'nri_cf': round(nri_idi['nri_cf'], 3),
        'nri_cf_se': round(nri_idi['nri_cf_se'], 3),
        'nri_cf_p': round(nri_idi['nri_cf_p'], 4),
        'nri_e': round(nri_idi['nri_e'], 3),
        'nri_ne': round(nri_idi['nri_ne'], 3),
        'idi': round(nri_idi['idi'], 3),
        'idi_se': round(nri_idi['idi_se'], 3),
        'idi_p': round(nri_idi['idi_p'], 4),
    },
    'dsi_quartile_mortality': {},
}

# Add quartile mortality
for q in ['Q1', 'Q2', 'Q3', 'Q4']:
    n = len(cc_analysis[cc_analysis['dsi_quartile'] == q])
    deaths = cc_analysis[cc_analysis['dsi_quartile'] == q]['mortality'].sum()
    rate = round(deaths / n * 100, 1) if n > 0 else 0
    results['dsi_quartile_mortality'][q] = {'n': n, 'deaths': int(deaths), 'rate_pct': rate}

# Save
with open(os.path.join(OUTPUT_DIR, 'eicu_external_validation_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

cc_analysis.to_csv(os.path.join(OUTPUT_DIR, 'eicu_external_validation_dataset.csv'), index=False)

print(f"\n    Results saved to: {OUTPUT_DIR}/eicu_external_validation_results.json")
print(f"    Dataset saved to: {OUTPUT_DIR}/eicu_external_validation_dataset.csv")

# ── Summary ──────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  EXTERNAL VALIDATION SUMMARY")
print("=" * 70)
print(f"  eICU cohort: N={len(cc_analysis):,}, mortality={cc_analysis['mortality'].mean()*100:.1f}%")
print(f"  MIMIC-IV → eICU AUC change: Ext {auc_ext:.3f}, Ext+DSI {auc_ext_dsi:.3f}")
print(f"  ΔAUC in eICU: {delta_auc:.4f} (DeLong P={p_delong:.4f})")
print(f"  cf-NRI: {nri_idi['nri_cf']:.3f} (P={nri_idi['nri_cf_p']:.4f})")
print(f"  IDI: {nri_idi['idi']:.3f} (P={nri_idi['idi_p']:.4f})")
print(f"  Calibration (raw): Ext Brier={brier_ext_raw:.4f}, Ext+DSI Brier={brier_ext_dsi_raw:.4f}")
print(f"  Calibration (recal): Ext Brier={brier_ext_recal:.4f} HL P={hl_p_ext_recal:.3f}")
print(f"  Calibration (recal): Ext+DSI Brier={brier_ext_dsi_recal:.4f} HL P={hl_p_dsi_recal:.3f}")
print(f"  DSI quartile gradient (eICU):")
for q in ['Q1', 'Q2', 'Q3', 'Q4']:
    n = len(cc_analysis[cc_analysis['dsi_quartile'] == q])
    deaths = cc_analysis[cc_analysis['dsi_quartile'] == q]['mortality'].sum()
    rate = deaths / n * 100 if n > 0 else 0
    print(f"    {q}: {rate:.1f}%")
print("=" * 70)
