"""
Recompute all models with SOFA added to extended baseline.
Includes: AUC, NRI (categorical + category-free), IDI with bootstrap 95% CIs,
DSI quartile cutoffs, subgroup AUCs, and surgery timing sensitivity.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score, roc_curve
from scipy.stats import mannwhitneyu
import duckdb
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = "C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen"

# Load data with SOFA
df = pd.read_csv(f"{OUTPUT_DIR}/analysis_dataset_with_sofa.csv")
cc = df.copy()  # already CC (filtered in extract_sofa.py)
y = cc['hospital_expire_flag'].values
N = len(cc)
print(f"CC cohort: N={N}, mortality={y.sum()} ({y.mean()*100:.1f}%)")
print(f"SOFA: median {cc['sofa'].median():.1f} [IQR {cc['sofa'].quantile(0.25):.0f}-{cc['sofa'].quantile(0.75):.0f}]")

# ============================================================
# 1. DSI Quartile Cutoffs
# ============================================================
print("\n" + "="*60)
print("1. DSI Quartile Cutoffs")
print("="*60)
q = cc['DSI_mean'].quantile([0.25, 0.5, 0.75])
print(f"Q1 < {q[0.25]:.3f}")
print(f"Q2 {q[0.25]:.3f} - {q[0.5]:.3f}")
print(f"Q3 {q[0.5]:.3f} - {q[0.75]:.3f}")
print(f"Q4 > {q[0.75]:.3f}")

# Quartile mortality
cc['dsi_quartile'] = pd.qcut(cc['DSI_mean'], 4, labels=['Q1','Q2','Q3','Q4'])
for q_label in ['Q1','Q2','Q3','Q4']:
    sub = cc[cc['dsi_quartile']==q_label]
    print(f"  {q_label}: N={len(sub)}, mortality={sub['hospital_expire_flag'].sum()} ({sub['hospital_expire_flag'].mean()*100:.1f}%)")

# ============================================================
# 2. Model Definitions
# ============================================================
print("\n" + "="*60)
print("2. Model Comparison (with SOFA)")
print("="*60)

# Basic model (SI derivatives only)
X_basic = cc[['SI_mean']].copy()
X_basic = sm.add_constant(X_basic)

# Extended baseline (original + SOFA)
X_ext = cc[['age_at_admission','gender','CCI','lactate_first','wbc_first',
            'vasopressor_use','any_surgery','mechanical_ventilation','sofa']].copy()
X_ext['gender'] = (X_ext['gender']=='M').astype(int)
X_ext = sm.add_constant(X_ext)

# Extended + DSI
X_dsi = X_ext.copy()
X_dsi['DSI'] = cc['DSI_mean'].values

# Extended + all 4 SI derivatives
X_full = X_ext.copy()
for col in ['SI_mean','MSI_mean','DSI_mean','Age_SI_mean']:
    X_full[col] = cc[col].values

# Fit models
models = {}
predictions = {}

for name, X in [('Basic (SI)', X_basic), ('Extended+SOFA', X_ext), 
                 ('Extended+SOFA+DSI', X_dsi), ('Extended+SOFA+All SI', X_full)]:
    model = sm.Logit(y, X).fit(disp=0, maxiter=5000)
    pred = model.predict(X)
    auc = roc_auc_score(y, pred)
    models[name] = model
    predictions[name] = pred
    print(f"  {name}: AUC = {auc:.4f}")

# ============================================================
# 3. NRI and IDI with Bootstrap 95% CIs
# ============================================================
print("\n" + "="*60)
print("3. NRI and IDI (Extended+SOFA → Extended+SOFA+DSI)")
print("="*60)

p_old = predictions['Extended+SOFA'].values
p_new = predictions['Extended+SOFA+DSI'].values

def nri_categorical(y, p_old, p_new, thresholds=[0.1, 0.3]):
    cats_old = np.digitize(p_old, thresholds)
    cats_new = np.digitize(p_new, thresholds)
    events = y == 1
    non_events = y == 0
    
    up_events = ((cats_new > cats_old) & events).sum()
    down_events = ((cats_new < cats_old) & events).sum()
    nri_event = (up_events - down_events) / events.sum()
    
    down_nonevents = ((cats_new < cats_old) & non_events).sum()
    up_nonevents = ((cats_new > cats_old) & non_events).sum()
    nri_nonevent = (down_nonevents - up_nonevents) / non_events.sum()
    
    return nri_event + nri_nonevent, nri_event, nri_nonevent

def nri_category_free(y, p_old, p_new):
    events = y == 1
    non_events = y == 0
    up_events = (p_new > p_old)[events].sum()
    down_events = (p_new < p_old)[events].sum()
    nri_event = (up_events - down_events) / events.sum()
    
    down_nonevents = (p_new < p_old)[non_events].sum()
    up_nonevents = (p_new > p_old)[non_events].sum()
    nri_nonevent = (down_nonevents - up_nonevents) / non_events.sum()
    
    return nri_event + nri_nonevent, nri_event, nri_nonevent

def calc_idi(y, p_old, p_new):
    events = y == 1
    non_events = y == 0
    idi = (np.mean(p_new[events]) - np.mean(p_old[events])) - \
          (np.mean(p_new[non_events]) - np.mean(p_old[non_events]))
    return idi

# Point estimates
nri_cat, nri_cat_e, nri_cat_ne = nri_categorical(y, p_old, p_new)
nri_cf, nri_cf_e, nri_cf_ne = nri_category_free(y, p_old, p_new)
idi = calc_idi(y, p_old, p_new)

print(f"Categorical NRI (10%/30%): {nri_cat:.4f} (events={nri_cat_e:.4f}, non-events={nri_cat_ne:.4f})")
print(f"Category-free NRI: {nri_cf:.4f} (events={nri_cf_e:.4f}, non-events={nri_cf_ne:.4f})")
print(f"IDI: {idi:.4f}")

# Bootstrap CIs
print("\nBootstrapping 95% CIs (1000 iterations)...")
n_boot = 1000
nri_cat_boot = []
nri_cf_boot = []
idi_boot = []
np.random.seed(42)

for i in range(n_boot):
    idx = np.random.choice(N, N, replace=True)
    try:
        b_old = sm.Logit(y[idx], X_ext.iloc[idx]).fit(disp=0, maxiter=200)
        b_new = sm.Logit(y[idx], X_dsi.iloc[idx]).fit(disp=0, maxiter=200)
        pb_old = b_old.predict(X_ext.iloc[idx]).values
        pb_new = b_new.predict(X_dsi.iloc[idx]).values
        
        nc, _, _ = nri_categorical(y[idx], pb_old, pb_new)
        ncf, _, _ = nri_category_free(y[idx], pb_old, pb_new)
        bi = calc_idi(y[idx], pb_old, pb_new)
        
        nri_cat_boot.append(nc)
        nri_cf_boot.append(ncf)
        idi_boot.append(bi)
    except:
        pass

nri_cat_boot = np.array(nri_cat_boot)
nri_cf_boot = np.array(nri_cf_boot)
idi_boot = np.array(idi_boot)

print(f"\nSuccessful bootstraps: {len(nri_cat_boot)}")
print(f"Categorical NRI: {nri_cat:.4f} (95% CI: {np.percentile(nri_cat_boot, 2.5):.4f} - {np.percentile(nri_cat_boot, 97.5):.4f})")
print(f"Category-free NRI: {nri_cf:.4f} (95% CI: {np.percentile(nri_cf_boot, 2.5):.4f} - {np.percentile(nri_cf_boot, 97.5):.4f})")
print(f"IDI: {idi:.4f} (95% CI: {np.percentile(idi_boot, 2.5):.4f} - {np.percentile(idi_boot, 97.5):.4f})")

# ============================================================
# 4. DSI Odds Ratio (Extended+SOFA+DSI model)
# ============================================================
print("\n" + "="*60)
print("4. DSI Odds Ratio (Extended+SOFA+DSI)")
print("="*60)
dsi_model = models['Extended+SOFA+DSI']
or_dsi = np.exp(dsi_model.params['DSI'])
ci_lo = np.exp(dsi_model.conf_int().loc['DSI', 0])
ci_hi = np.exp(dsi_model.conf_int().loc['DSI', 1])
p_dsi = dsi_model.pvalues['DSI']
print(f"DSI OR: {or_dsi:.3f} (95% CI: {ci_lo:.3f} - {ci_hi:.3f}), P = {p_dsi:.2e}")

# Full model coefficients
print("\nFull model coefficients (Extended+SOFA+DSI):")
for var in dsi_model.params.index:
    if var == 'const':
        print(f"  Intercept: {dsi_model.params[var]:.4f}")
    else:
        print(f"  {var}: OR={np.exp(dsi_model.params[var]):.3f} (95% CI: {np.exp(dsi_model.conf_int().loc[var, 0]):.3f}-{np.exp(dsi_model.conf_int().loc[var, 1]):.3f}), P={dsi_model.pvalues[var]:.2e}")

# ============================================================
# 5. Subgroup AUCs
# ============================================================
print("\n" + "="*60)
print("5. Subgroup AUCs (Extended+SOFA+DSI)")
print("="*60)

subtypes = cc['abdomen_subtype'].unique()
for st in sorted(subtypes):
    sub = cc[cc['abdomen_subtype']==st]
    if len(sub) < 20 or sub['hospital_expire_flag'].nunique() < 2:
        print(f"  {st}: N={len(sub)} (insufficient)")
        continue
    X_sub = X_dsi.loc[sub.index]
    y_sub = sub['hospital_expire_flag'].values
    try:
        m = sm.Logit(y_sub, X_sub).fit(disp=0, maxiter=5000)
        p_sub = m.predict(X_sub)
        auc_sub = roc_auc_score(y_sub, p_sub)
        print(f"  {st}: N={len(sub)}, mortality={y_sub.mean()*100:.1f}%, AUC={auc_sub:.4f}")
    except:
        print(f"  {st}: N={len(sub)}, model failed to converge")

# Surgical vs non-surgical (drop any_surgery from model to avoid collinearity)
X_dsi_nosurg = X_dsi.drop(columns=['any_surgery'])
for surg_label, surg_val in [('Surgical', 1), ('Non-surgical', 0)]:
    sub = cc[cc['any_surgery']==surg_val]
    X_sub = X_dsi_nosurg.loc[sub.index]
    y_sub = sub['hospital_expire_flag'].values
    try:
        m = sm.Logit(y_sub, X_sub).fit(disp=0, maxiter=5000)
        p_sub = m.predict(X_sub)
        auc_sub = roc_auc_score(y_sub, p_sub)
        or_sub = np.exp(m.params['DSI'])
        print(f"  {surg_label}: N={len(sub)}, mortality={y_sub.mean()*100:.1f}%, AUC={auc_sub:.4f}, DSI OR={or_sub:.3f}")
    except:
        print(f"  {surg_label}: model failed")

# ============================================================
# 6. Surgery Timing Fix (≤24h)
# ============================================================
print("\n" + "="*60)
print("6. Surgery Timing: Redefining as ≤24h from ICU admission")
print("="*60)

DATA_DIR = "E:/mimic-iv/v3.1/physionet.org/files/mimiciv/3.1"
con = duckdb.connect()

# Register cc_ids BEFORE querying
cc_ids_df = cc[['stay_id', 'hadm_id']].drop_duplicates()
con.register('cc_ids_placeholder', cc_ids_df)

# Get icustays intime for our cohort
icustays = con.execute(f"""
    SELECT stay_id, hadm_id, intime
    FROM read_csv_auto('{DATA_DIR}/icu/icustays.csv.gz')
    WHERE stay_id IN (SELECT stay_id FROM cc_ids_placeholder)
""").fetchdf()

# Get procedures_icd with chartdate
# Abdominal surgery ICD-10 codes (same as original analysis)
abdomen_surg_icd10 = [
    # Perforation
    '0DTJ4ZZ', '0DTJ0ZZ', '0DTJ3ZZ', '0DTJ4Z1',
    # Ischemia  
    '0DB68ZZ', '0DB60ZZ', '0DB63ZZ',
    # Obstruction
    '0DB68ZX', '0DB60ZX',
    # General abdominal
    '0W110J4', '0W110J3', '0W110F4', '0W110F3',
    '0DJ08ZZ', '0DJ08ZX', '0DJ08Z7',
    '0DB98ZX', '0DB90ZX',
    '0DT04ZZ', '0DT00ZZ', '0DT03ZZ',
    '0VP60ZZ', '0VP64ZZ',
]

# Also ICD-9 if any (older records)
abdomen_surg_icd9 = [
    '45.61', '45.62', '45.71', '45.72', '45.73', '45.74', '45.75', '45.76', '45.79', '45.8',
    '46.01', '46.02', '46.03', '46.10', '46.11', '46.20', '46.21', '46.22', '46.23', '46.30', '46.31', '46.32', '46.33', '46.39', '46.41', '46.42', '46.43', '46.50', '46.51', '46.52', '46.53', '46.59', '46.60', '46.61', '46.62', '46.63', '46.69', '46.70', '46.71', '46.72', '46.73', '46.74', '46.75', '46.76', '46.79', '46.80', '46.81', '46.82', '46.83', '46.86', '46.87', '46.91', '46.92', '46.93', '46.94', '46.99',
    '47.01', '47.02', '47.05', '47.06', '47.09', '47.11', '47.19', '47.21', '47.29',
    '48.40', '48.41', '48.42', '48.43', '48.50', '48.51', '48.52', '48.59', '48.61', '48.62', '48.63', '48.69',
    '54.0', '54.1', '54.11', '54.12', '54.13', '54.19', '54.21', '54.22', '54.23', '54.24', '54.25', '54.29', '54.31', '54.39', '54.4', '54.41', '54.42', '54.43', '54.49', '54.51', '54.52', '54.59', '54.61', '54.62', '54.63', '54.64', '54.69', '54.71', '54.72', '54.73', '54.74', '54.79', '54.91', '54.92', '54.93', '54.94', '54.95', '54.98', '54.99',
]

# Query procedures_icd
all_codes = abdomen_surg_icd10 + abdomen_surg_icd9
codes_str = ",".join([f"'{c}'" for c in all_codes])

procs = con.execute(f"""
    SELECT pi.hadm_id, pi.chartdate, pi.icd_code, pi.icd_version
    FROM read_csv_auto('{DATA_DIR}/hosp/procedures_icd.csv.gz') pi
    INNER JOIN (SELECT DISTINCT hadm_id FROM cc_ids_placeholder) ci
        ON pi.hadm_id = ci.hadm_id
    WHERE pi.icd_code IN ({codes_str})
""").fetchdf()
con.close()

print(f"Found {len(procs)} abdominal surgery procedures for cohort")

# Match with ICU intime
procs = procs.merge(icustays[['stay_id', 'hadm_id', 'intime']], on='hadm_id', how='inner')
procs['chartdate'] = pd.to_datetime(procs['chartdate'])
procs['intime'] = pd.to_datetime(procs['intime'])

# Surgery within 1 day of ICU admission (≤24h approximation)
procs['days_from_icu'] = (procs['chartdate'] - procs['intime']).dt.days
# ≤24h means same day or next day (0 or 1)
procs_early = procs[procs['days_from_icu'].between(-1, 1)]

# Get stay_ids with early surgery
early_surgery_stays = procs_early['stay_id'].unique()
print(f"Stays with surgery ≤24h: {len(early_surgery_stays)}")
print(f"Original any_surgery=1: {cc['any_surgery'].sum()}")

# Create new surgery variable
cc['surgery_24h'] = cc['stay_id'].isin(early_surgery_stays).astype(int)
print(f"Surgery ≤24h: {cc['surgery_24h'].sum()} ({cc['surgery_24h'].mean()*100:.1f}%)")
print(f"Surgery during hospitalization: {cc['any_surgery'].sum()} ({cc['any_surgery'].mean()*100:.1f}%)")

# Recompute model with surgery_24h
X_ext_24h = cc[['age_at_admission','gender','CCI','lactate_first','wbc_first',
                'vasopressor_use','surgery_24h','mechanical_ventilation','sofa']].copy()
X_ext_24h['gender'] = (X_ext_24h['gender']=='M').astype(int)
X_ext_24h = sm.add_constant(X_ext_24h)

X_dsi_24h = X_ext_24h.copy()
X_dsi_24h['DSI'] = cc['DSI_mean'].values

m_ext_24h = sm.Logit(y, X_ext_24h).fit(disp=0, maxiter=5000)
m_dsi_24h = sm.Logit(y, X_dsi_24h).fit(disp=0, maxiter=5000)

auc_ext_24h = roc_auc_score(y, m_ext_24h.predict(X_ext_24h))
auc_dsi_24h = roc_auc_score(y, m_dsi_24h.predict(X_dsi_24h))
print(f"\nWith surgery ≤24h:")
print(f"  Extended+SOFA AUC: {auc_ext_24h:.4f}")
print(f"  Extended+SOFA+DSI AUC: {auc_dsi_24h:.4f}")
print(f"  Delta AUC: {auc_dsi_24h - auc_ext_24h:.4f}")

or_dsi_24h = np.exp(m_dsi_24h.params['DSI'])
print(f"  DSI OR: {or_dsi_24h:.3f} (95% CI: {np.exp(m_dsi_24h.conf_int().loc['DSI', 0]):.3f}-{np.exp(m_dsi_24h.conf_int().loc['DSI', 1]):.3f})")

# ============================================================
# 7. Bootstrap Validation (Optimism)
# ============================================================
print("\n" + "="*60)
print("7. Bootstrap Validation (Extended+SOFA+DSI)")
print("="*60)

n_boot_val = 200
auc_apparent = roc_auc_score(y, m_dsi_24h.predict(X_dsi_24h))
auc_boot_list = []
auc_orig_list = []
np.random.seed(42)

for i in range(n_boot_val):
    idx = np.random.choice(N, N, replace=True)
    try:
        b_model = sm.Logit(y[idx], X_dsi_24h.iloc[idx]).fit(disp=0, maxiter=300)
        # AUC on bootstrap sample (apparent)
        p_boot = b_model.predict(X_dsi_24h.iloc[idx])
        auc_boot = roc_auc_score(y[idx], p_boot)
        # AUC on original sample (test)
        p_orig = b_model.predict(X_dsi_24h)
        auc_orig = roc_auc_score(y, p_orig)
        auc_boot_list.append(auc_boot)
        auc_orig_list.append(auc_orig)
    except:
        pass

auc_boot_arr = np.array(auc_boot_list)
auc_orig_arr = np.array(auc_orig_list)
optimism = (auc_boot_arr - auc_orig_arr).mean()
auc_corrected = auc_apparent - optimism
print(f"Apparent AUC: {auc_apparent:.4f}")
print(f"Bootstrap mean AUC: {auc_boot_arr.mean():.4f}")
print(f"Original sample mean AUC: {auc_orig_arr.mean():.4f}")
print(f"Optimism: {optimism:.4f}")
print(f"Corrected AUC: {auc_corrected:.4f}")

# ============================================================
# 8. Multiple Imputation (MICE)
# ============================================================
print("\n" + "="*60)
print("8. Multiple Imputation Sensitivity Analysis")
print("="*60)

# Load FULL dataset (not just CC)
df_full = pd.read_csv(f"{OUTPUT_DIR}/analysis_dataset_corrected.csv")
print(f"Full dataset: N={len(df_full)}")
print(f"Missing lactate: {df_full['lactate_first'].isna().sum()} ({df_full['lactate_first'].isna().mean()*100:.1f}%)")
print(f"Missing WBC: {df_full['wbc_first'].isna().sum()} ({df_full['wbc_first'].isna().mean()*100:.1f}%)")

# Merge SOFA to full dataset
sofa_scores = pd.read_csv(f"{OUTPUT_DIR}/sofa_scores.csv")
df_full = df_full.merge(sofa_scores[['stay_id', 'sofa']], on='stay_id', how='left')
print(f"SOFA missing in full dataset: {df_full['sofa'].isna().sum()}")

# Simple imputation using sklearn IterativeImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Variables to impute
impute_cols = ['age_at_admission','CCI','lactate_first','wbc_first','sofa','DSI_mean',
               'SI_mean','MSI_mean','Age_SI_mean','MAP_min','HR_mean','SBP_mean','DBP_mean']
impute_df = df_full[impute_cols].copy()

# Gender and binary vars
impute_df['gender_M'] = (df_full['gender']=='M').astype(int)
impute_df['vasopressor_use'] = df_full['vasopressor_use']
impute_df['any_surgery'] = df_full['any_surgery']
impute_df['mechanical_ventilation'] = df_full['mechanical_ventilation']
impute_df['hospital_expire_flag'] = df_full['hospital_expire_flag']

# Single imputation for speed (MICE with 1 iteration as approximation)
# Full MICE would do 20 imputations, but for sensitivity check 5 is enough
n_imputations = 5
auc_mi_list = []
or_mi_list = []

for mi in range(n_imputations):
    np.random.seed(mi * 100 + 42)
    imputer = IterativeImputer(max_iter=10, random_state=mi*100+42, sample_posterior=True)
    imputed = imputer.fit_transform(impute_df)
    imp_df = pd.DataFrame(imputed, columns=impute_df.columns)
    
    y_mi = imp_df['hospital_expire_flag'].values.astype(int)
    X_mi = imp_df[['age_at_admission','gender_M','CCI','lactate_first','wbc_first',
                   'vasopressor_use','any_surgery','mechanical_ventilation','sofa']].copy()
    X_mi = sm.add_constant(X_mi)
    X_mi['DSI'] = imp_df['DSI_mean'].values
    
    try:
        m = sm.Logit(y_mi, X_mi).fit(disp=0, maxiter=5000)
        p = m.predict(X_mi)
        auc = roc_auc_score(y_mi, p)
        or_val = np.exp(m.params['DSI'])
        auc_mi_list.append(auc)
        or_mi_list.append(or_val)
        print(f"  Imputation {mi+1}: AUC={auc:.4f}, DSI OR={or_val:.3f}")
    except:
        print(f"  Imputation {mi+1}: failed")

if auc_mi_list:
    print(f"\nMultiple Imputation Summary ({len(auc_mi_list)} imputations):")
    print(f"  AUC: {np.mean(auc_mi_list):.4f} ± {np.std(auc_mi_list):.4f}")
    print(f"  DSI OR: {np.mean(or_mi_list):.3f} ± {np.std(or_mi_list):.3f}")

# ============================================================
# 9. ICU Type Sensitivity (MICU/SICU/TSICU only)
# ============================================================
print("\n" + "="*60)
print("9. ICU Type Sensitivity (MICU/SICU/TSICU)")
print("="*60)

icu_types = cc['first_careunit'].value_counts()
print("ICU type distribution:")
print(icu_types)

micu_sicu = cc[cc['first_careunit'].isin(['Medical Intensive Care Unit (MICU)', 
                                            'Surgical Intensive Care Unit (SICU)',
                                            'Trauma SICU (TSICU)'])]
print(f"\nMICU/SICU/TSICU: N={len(micu_sicu)}, mortality={micu_sicu['hospital_expire_flag'].mean()*100:.1f}%")

if len(micu_sicu) > 50 and micu_sicu['hospital_expire_flag'].nunique() > 1:
    X_mi_icu = X_dsi.loc[micu_sicu.index]
    y_mi_icu = micu_sicu['hospital_expire_flag'].values
    try:
        m = sm.Logit(y_mi_icu, X_mi_icu).fit(disp=0, maxiter=5000)
        p = m.predict(X_mi_icu)
        auc = roc_auc_score(y_mi_icu, p)
        or_val = np.exp(m.params['DSI'])
        print(f"  AUC={auc:.4f}, DSI OR={or_val:.3f}")
    except:
        print("  Model failed to converge")

# ============================================================
# 10. Save Summary
# ============================================================
print("\n" + "="*60)
print("10. Saving Summary Results")
print("="*60)

summary = {
    'metric': [
        'N (CC)', 'Mortality (%)', 'SOFA median [IQR]',
        'Extended+SOFA AUC', 'Extended+SOFA+DSI AUC', 'Delta AUC',
        'Categorical NRI', 'NRI 95% CI lo', 'NRI 95% CI hi',
        'Category-free NRI', 'CF-NRI 95% CI lo', 'CF-NRI 95% CI hi',
        'IDI', 'IDI 95% CI lo', 'IDI 95% CI hi',
        'DSI OR', 'DSI OR 95% CI lo', 'DSI OR 95% CI hi', 'DSI P',
        'Surgery ≤24h AUC (Extended+DSI)', 'Surgery ≤24h DSI OR',
        'Apparent AUC (bootstrap val)', 'Optimism', 'Corrected AUC',
        'MI AUC mean', 'MI DSI OR mean',
    ],
    'value': [
        N, f"{y.mean()*100:.1f}%", f"{cc['sofa'].median():.1f} [{cc['sofa'].quantile(0.25):.0f}-{cc['sofa'].quantile(0.75):.0f}]",
        f"{roc_auc_score(y, predictions['Extended+SOFA']):.4f}",
        f"{roc_auc_score(y, predictions['Extended+SOFA+DSI']):.4f}",
        f"{roc_auc_score(y, predictions['Extended+SOFA+DSI']) - roc_auc_score(y, predictions['Extended+SOFA']):.4f}",
        f"{nri_cat:.4f}", f"{np.percentile(nri_cat_boot, 2.5):.4f}", f"{np.percentile(nri_cat_boot, 97.5):.4f}",
        f"{nri_cf:.4f}", f"{np.percentile(nri_cf_boot, 2.5):.4f}", f"{np.percentile(nri_cf_boot, 97.5):.4f}",
        f"{idi:.4f}", f"{np.percentile(idi_boot, 2.5):.4f}", f"{np.percentile(idi_boot, 97.5):.4f}",
        f"{or_dsi:.3f}", f"{ci_lo:.3f}", f"{ci_hi:.3f}", f"{p_dsi:.2e}",
        f"{auc_dsi_24h:.4f}", f"{or_dsi_24h:.3f}",
        f"{auc_apparent:.4f}", f"{optimism:.4f}", f"{auc_corrected:.4f}",
        f"{np.mean(auc_mi_list):.4f}" if auc_mi_list else "N/A",
        f"{np.mean(or_mi_list):.3f}" if or_mi_list else "N/A",
    ]
}
summary_df = pd.DataFrame(summary)
summary_df.to_csv(f"{OUTPUT_DIR}/revised_analysis_summary.csv", index=False)
print("Saved revised_analysis_summary.csv")

# Save updated dataset with surgery_24h
cc.to_csv(f"{OUTPUT_DIR}/analysis_dataset_revised.csv", index=False)
print("Saved analysis_dataset_revised.csv")

print("\n✅ All recomputations complete!")
