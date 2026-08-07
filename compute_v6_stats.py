"""
Compute additional statistics required by AIC v6 peer review:
P0-2: Excluded patient characteristics (N=3205 vs CC N=5728)
P0-4: Model without surgery; model with surgery_24h as primary
P1-4: Parsimonious model (without vasopressor, MV, gender)
P0-5: Sensitivity excluding Other subtype
P0-6: Un-recalibrated eICU metrics (already in JSON)
General: All new model AUCs + coefficients
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss
# from sklearn.impute import IterativeImputer  # not needed for this script
import json
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE = r"C:\Users\admin\WorkBuddy\2026-07-07-20-09-20\shock_index_abdomen"
CC_FILE = f"{BASE}\\analysis_dataset_revised.csv"
FULL_FILE = f"{BASE}\\analysis_dataset_extended.csv"

# Load data
cc = pd.read_csv(CC_FILE)
full = pd.read_csv(FULL_FILE)

# Merge SOFA into full dataset (from CC dataset)
sofa_map = cc[['stay_id', 'sofa', 'dsi_quartile', 'surgery_24h']].set_index('stay_id')
full = full.join(sofa_map, on='stay_id', how='left')

# ============================================================
# P0-2: Excluded vs CC patient characteristics
# ============================================================
excluded_ids = set(full['stay_id']) - set(cc['stay_id'])
excluded = full[full['stay_id'].isin(excluded_ids)]

def describe_group(df, label):
    stats = {}
    stats['N'] = len(df)
    stats['Age_median'] = df['age_at_admission'].median()
    stats['Age_IQR'] = f"{df['age_at_admission'].quantile(0.25)}-{df['age_at_admission'].quantile(0.75)}"
    stats['Male_pct'] = (df['gender'] == 'M').mean() * 100
    stats['Mortality_pct'] = df['hospital_expire_flag'].mean() * 100 if 'hospital_expire_flag' in df.columns else df['hospital_death'].mean() * 100
    stats['Vasopressor_pct'] = df['vasopressor_use'].mean() * 100
    stats['MV_pct'] = df['mechanical_ventilation'].mean() * 100
    stats['Surgery_pct'] = df['any_surgery'].mean() * 100
    stats['Lactate_available_pct'] = df['lactate_first'].notna().mean() * 100
    stats['WBC_available_pct'] = df['wbc_first'].notna().mean() * 100
    stats['DSI_mean_available'] = df['DSI_mean'].notna().mean() * 100
    
    # For fields that may be NaN in excluded group
    if df['lactate_first'].notna().any():
        stats['Lactate_median'] = df['lactate_first'].median()
    else:
        stats['Lactate_median'] = 'N/A'
    
    if df['sofa'].notna().any():
        stats['SOFA_median'] = df['sofa'].median()
        stats['SOFA_IQR'] = f"{df['sofa'].quantile(0.25)}-{df['sofa'].quantile(0.75)}"
    else:
        stats['SOFA_median'] = 'N/A'
        stats['SOFA_IQR'] = 'N/A'
    
    return stats

cc_stats = describe_group(cc, 'CC')
ex_stats = describe_group(excluded, 'Excluded')

print("=" * 80)
print("P0-2: Excluded vs CC Patient Characteristics")
print("=" * 80)
for key in cc_stats:
    print(f"  {key}: CC={cc_stats[key]}, Excluded={ex_stats[key]}")

# ============================================================
# Model computation helper
# ============================================================
def compute_model(df, predictors, outcome='hospital_expire_flag', label=''):
    """Fit logistic regression, return AUC, coefficients, DeLong-ready stats"""
    df_model = df[predictors + [outcome]].dropna()
    X = df_model[predictors].values
    y = df_model[outcome].values
    
    lr = LogisticRegression(max_iter=5000, solver='lbfgs')
    lr.fit(X, y)
    
    y_pred_prob = lr.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, y_pred_prob)
    brier = brier_score_loss(y, y_pred_prob)
    
    # Get coefficients with SE
    from scipy import stats
    coef = lr.coef_[0]
    intercept = lr.intercept_[0]
    
    # Compute SE from fisher information
    X_design = np.column_stack([np.ones(len(X)), X])
    prob = y_pred_prob
    W = prob * (1 - prob)
    fisher = np.dot(X_design.T * W, X_design)
    try:
        cov = np.linalg.inv(fisher)
        se = np.sqrt(np.diag(cov))
    except:
        se = np.array([np.nan] * (len(coef) + 1))
    
    # OR and CI
    results = {
        'label': label,
        'N': len(df_model),
        'n_events': int(y.sum()),
        'AUC': round(auc, 4),
        'Brier': round(brier, 4),
        'intercept': round(intercept, 4),
        'intercept_se': round(se[0], 4),
        'predictors': predictors,
        'coefficients': {}
    }
    
    for i, p in enumerate(predictors):
        or_val = np.exp(coef[i])
        ci_lower = np.exp(coef[i] - 1.96 * se[i+1])
        ci_upper = np.exp(coef[i] + 1.96 * se[i+1])
        p_val = 2 * stats.norm.sf(abs(coef[i] / se[i+1])) if se[i+1] > 0 else np.nan
        
        results['coefficients'][p] = {
            'beta': round(coef[i], 4),
            'se': round(se[i+1], 4),
            'OR': round(or_val, 4),
            'CI_lower': round(ci_lower, 4),
            'CI_upper': round(ci_upper, 4),
            'P': f"{p_val:.2e}" if p_val < 0.001 else round(p_val, 4)
        }
    
    return results

# Common predictor sets
BASIC = ['age_at_admission', 'gender_binary', 'CCI']
EXTENDED = BASIC + ['lactate_first', 'wbc_first', 'vasopressor_use', 'any_surgery', 'mechanical_ventilation', 'sofa']
EXTENDED_NO_SURG = BASIC + ['lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'sofa']
EXTENDED_SURG24H = BASIC + ['lactate_first', 'wbc_first', 'vasopressor_use', 'surgery_24h', 'mechanical_ventilation', 'sofa']
PARSIMONIOUS = BASIC + ['lactate_first', 'wbc_first', 'sofa']  # no vasopressor, MV, gender
EXTENDED_NO_VMVG = BASIC + ['lactate_first', 'wbc_first', 'any_surgery', 'sofa']  # no vasopressor, MV, but keep gender as binary

# Prepare binary gender
cc['gender_binary'] = (cc['gender'] == 'M').astype(int)

# ============================================================
# P0-4: Models with surgery variations
# ============================================================
print("\n" + "=" * 80)
print("P0-4: Surgery Variations")
print("=" * 80)

# 1. Extended + DSI (original with surgery)
r_ext_dsi = compute_model(cc, EXTENDED + ['DSI_mean'], label='Extended+DSI (with surgery)')
print(f"  Extended+DSI (with surgery): AUC={r_ext_dsi['AUC']}, N={r_ext_dsi['N']}")

# 2. Extended_no_surgery + DSI
r_nosurg_dsi = compute_model(cc, EXTENDED_NO_SURG + ['DSI_mean'], label='Extended_no_surgery+DSI')
print(f"  Extended_no_surgery+DSI: AUC={r_nosurg_dsi['AUC']}, N={r_nosurg_dsi['N']}")

# 3. Extended with surgery_24h + DSI
r_surg24h_dsi = compute_model(cc, EXTENDED_SURG24H + ['DSI_mean'], label='Extended_surgery24h+DSI')
print(f"  Extended_surgery24h+DSI: AUC={r_surg24h_dsi['AUC']}, N={r_surg24h_dsi['N']}")

# 4. Extended baseline without surgery (for comparison)
r_nosurg_base = compute_model(cc, EXTENDED_NO_SURG, label='Extended_no_surgery baseline')
print(f"  Extended_no_surgery baseline: AUC={r_nosurg_base['AUC']}")

# 5. Extended with surgery baseline (original)
r_ext_base = compute_model(cc, EXTENDED, label='Extended baseline (with surgery)')
print(f"  Extended baseline (with surgery): AUC={r_ext_base['AUC']}")

# ============================================================
# P1-4: Parsimonious models
# ============================================================
print("\n" + "=" * 80)
print("P1-4: Parsimonious Models")
print("=" * 80)

r_parsim_dsi = compute_model(cc, PARSIMONIOUS + ['DSI_mean'], label='Parsimonious+DSI (age+CCI+lactate+WBC+SOFA+DSI)')
print(f"  Parsimonious+DSI: AUC={r_parsim_dsi['AUC']}, N={r_parsim_dsi['N']}")

r_parsim_base = compute_model(cc, PARSIMONIOUS, label='Parsimonious baseline')
print(f"  Parsimonious baseline: AUC={r_parsim_base['AUC']}")

r_novmvg_dsi = compute_model(cc, EXTENDED_NO_VMVG + ['DSI_mean'], label='Extended_no_VMV+DSI (no vasopressor/MV)')
print(f"  Extended_no_VMV+DSI: AUC={r_novmvg_dsi['AUC']}, N={r_novmvg_dsi['N']}")

# ============================================================
# P0-5: Excluding Other subtype
# ============================================================
print("\n" + "=" * 80)
print("P0-5: Excluding Other Subtype")
print("=" * 80)

cc_no_other = cc[cc['abdomen_subtype'] != 'other']
r_noother_dsi = compute_model(cc_no_other, EXTENDED + ['DSI_mean'], label='Extended+DSI excluding Other')
print(f"  Extended+DSI (excl Other): AUC={r_noother_dsi['AUC']}, N={r_noother_dsi['N']}, n_events={r_noother_dsi['n_events']}")

r_noother_nosurg_dsi = compute_model(cc_no_other, EXTENDED_NO_SURG + ['DSI_mean'], label='Extended_no_surgery+DSI excl Other')
print(f"  Extended_no_surgery+DSI (excl Other): AUC={r_noother_nosurg_dsi['AUC']}")

# Also: restricted to primary acute abdomen subtypes only
cc_primary = cc[cc['abdomen_subtype'].isin(['inflammation', 'obstruction', 'perforation', 'ischemia'])]
r_primary_dsi = compute_model(cc_primary, EXTENDED + ['DSI_mean'], label='Extended+DSI primary subtypes only')
print(f"  Extended+DSI (primary subtypes only): AUC={r_primary_dsi['AUC']}, N={r_primary_dsi['N']}")

# ============================================================
# P0-6: Un-recalibrated eICU metrics
# ============================================================
print("\n" + "=" * 80)
print("P0-6: Un-recalibrated eICU Metrics (from existing JSON)")
print("=" * 80)

with open(f"{BASE}\\eicu_external_validation_results.json", 'r') as f:
    eicu_results = json.load(f)

print(f"  Raw Extended Brier: {eicu_results['calibration_raw']['extended_brier']}")
print(f"  Raw Extended HL P: {eicu_results['calibration_raw']['extended_hl_p']}")
print(f"  Raw Extended+DSI Brier: {eicu_results['calibration_raw']['extended_dsi_brier']}")
print(f"  Raw Extended+DSI HL P: {eicu_results['calibration_raw']['extended_dsi_hl_p']}")
print(f"  Recalibrated Extended Brier: {eicu_results['calibration_recalibrated']['extended_brier']}")
print(f"  Recalibrated Extended HL P: {eicu_results['calibration_recalibrated']['extended_hl_p']}")
print(f"  Recalibrated Extended+DSI Brier: {eicu_results['calibration_recalibrated']['extended_dsi_brier']}")
print(f"  Recalibrated Extended+DSI HL P: {eicu_results['calibration_recalibrated']['extended_dsi_hl_p']}")
print(f"  Recal intercept shift (Ext+DSI): {eicu_results['calibration_recalibrated']['recal_intercept_shift_dsi']}")
print(f"  Recal slope (Ext+DSI): {eicu_results['calibration_recalibrated']['recal_slope_dsi']}")

# ============================================================
# Delta AUC calculations
# ============================================================
print("\n" + "=" * 80)
print("Delta AUC Summary")
print("=" * 80)

# Without surgery
delta_nosurg = r_nosurg_dsi['AUC'] - r_nosurg_base['AUC']
print(f"  ΔAUC no_surgery: {r_nosurg_base['AUC']} → {r_nosurg_dsi['AUC']} (Δ={delta_nosurg})")

# With surgery (original)
delta_orig = r_ext_dsi['AUC'] - r_ext_base['AUC']
print(f"  ΔAUC with_surgery: {r_ext_base['AUC']} → {r_ext_dsi['AUC']} (Δ={delta_orig})")

# Parsimonious
delta_parsim = r_parsim_dsi['AUC'] - r_parsim_base['AUC']
print(f"  ΔAUC parsimonious: {r_parsim_base['AUC']} → {r_parsim_dsi['AUC']} (Δ={delta_parsim})")

# surgery_24h
r_surg24h_base = compute_model(cc, EXTENDED_SURG24H, label='Extended_surgery24h baseline')
delta_surg24h = r_surg24h_dsi['AUC'] - r_surg24h_base['AUC']
print(f"  ΔAUC surgery_24h: {r_surg24h_base['AUC']} → {r_surg24h_dsi['AUC']} (Δ={delta_surg24h})")

# ============================================================
# DSI OR in key models
# ============================================================
print("\n" + "=" * 80)
print("DSI OR in Key Models")
print("=" * 80)

for key_model in [r_ext_dsi, r_nosurg_dsi, r_surg24h_dsi, r_parsim_dsi, r_novmvg_dsi, r_noother_dsi, r_noother_nosurg_dsi, r_primary_dsi]:
    dsi_coef = key_model['coefficients'].get('DSI_mean', {})
    print(f"  {key_model['label']}: DSI OR={dsi_coef.get('OR', 'N/A')}, CI={dsi_coef.get('CI_lower', 'N/A')}-{dsi_coef.get('CI_upper', 'N/A')}, P={dsi_coef.get('P', 'N/A')}")

# Surgery OR comparison
for key_model in [r_ext_dsi, r_novmvg_dsi]:
    surg_coef = key_model['coefficients'].get('any_surgery', {})
    if surg_coef:
        print(f"  {key_model['label']}: Surgery OR={surg_coef.get('OR', 'N/A')}, P={surg_coef.get('P', 'N/A')}")

# ============================================================
# Full output JSON
# ============================================================
all_results = {
    'P0_2_excluded_vs_cc': {
        'CC': cc_stats,
        'Excluded': ex_stats
    },
    'P0_4_surgery_variations': {
        'extended_with_surgery_baseline': r_ext_base,
        'extended_with_surgery_DSI': r_ext_dsi,
        'extended_no_surgery_baseline': r_nosurg_base,
        'extended_no_surgery_DSI': r_nosurg_dsi,
        'extended_surgery24h_baseline': r_surg24h_base,
        'extended_surgery24h_DSI': r_surg24h_dsi,
    },
    'P1_4_parsimonious': {
        'parsimonious_baseline': r_parsim_base,
        'parsimonious_DSI': r_parsim_dsi,
        'extended_no_VMV_baseline': r_novmvg_dsi,  # this includes DSI already
    },
    'P0_5_subtype_exclusions': {
        'excl_other_DSI': r_noother_dsi,
        'excl_other_no_surgery_DSI': r_noother_nosurg_dsi,
        'primary_subtypes_only_DSI': r_primary_dsi,
    },
    'P0_6_eicu_unrecalibrated': eicu_results['calibration_raw'],
    'P0_6_eicu_recalibrated': eicu_results['calibration_recalibrated'],
    'delta_auc_summary': {
        'no_surgery': delta_nosurg,
        'with_surgery': delta_orig,
        'parsimonious': delta_parsim,
        'surgery_24h': delta_surg24h,
    }
}

output_file = f"{BASE}\\v6_revision_statistics.json"
with open(output_file, 'w') as f:
    json.dump(all_results, f, indent=2, default=str)

print(f"\nAll results saved to: {output_file}")
