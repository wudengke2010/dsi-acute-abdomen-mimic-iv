"""
Component Decomposition Analysis for v8 paper
Following Ospina-Tascón 2020 methodology:
1. AUC of individual components (HR, DBP, SBP, MAP) vs DSI ratio
2. DeLong comparison: each component vs DSI
3. Matched analysis: at similar HR or DBP, show DSI still predicts mortality
"""
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve
from scipy import stats
import json

BASE = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'

# Load dataset
df = pd.read_csv(f'{BASE}/analysis_dataset_revised.csv')
print(f"Dataset: {len(df)} rows, mortality {df['hospital_expire_flag'].mean()*100:.1f}%")

y = df['hospital_expire_flag'].values

# Component AUCs (mean 24h values)
components = {
    'HR (mean 24h)': df['HR_mean'].values,
    'DBP (mean 24h)': df['DBP_mean'].values,
    'SBP (mean 24h)': df['SBP_mean'].values,
    'MAP (mean 24h)': df['MAP_mean'].values,
    'SI (HR/SBP)': df['SI_mean'].values,
    'MSI (HR/MAP)': df['MSI_mean'].values,
    'DSI (HR/DBP)': df['DSI_mean'].values,
    'Age-SI': df['Age_SI_mean'].values,
    'SOFA': df['sofa'].values,
    'Lactate': df['lactate_first'].values,
}

# Compute AUC for each
# For BP components, lower values = worse → need to negate
results = {}
print("\n=== Individual AUC (unadjusted) ===")
for name, values in components.items():
    v = pd.Series(values).dropna()
    y_v = y[v.index]
    if len(v) == 0:
        continue
    auc = roc_auc_score(y_v, v)
    # For BP components, lower = worse, so AUC should be (1 - auc)
    if name in ['DBP (mean 24h)', 'SBP (mean 24h)', 'MAP (mean 24h)']:
        auc = 1 - auc  # flip so that higher AUC = better predictor
    results[name] = auc
    print(f"  {name}: AUC = {auc:.4f}")

# DeLong test function
def delong_test(y_true, y_pred1, y_pred2):
    """Simplified DeLong test using bootstrap."""
    n = len(y_true)
    n_boot = 500
    diffs = []
    for _ in range(n_boot):
        idx = np.random.choice(n, n, replace=True)
        try:
            auc1 = roc_auc_score(y_true[idx], y_pred1[idx])
            auc2 = roc_auc_score(y_true[idx], y_pred2[idx])
            # For BP, flip
            if y_pred1.mean() > 50 and np.corrcoef(y_pred1, y_true)[0,1] > 0:
                # positive correlation with death = high BP = more death? No, flip
                pass
            diffs.append(auc1 - auc2)
        except:
            pass
    diffs = np.array(diffs)
    se = np.std(diffs)
    if se == 0:
        return 1.0
    z = (roc_auc_score(y_true, y_pred1) - roc_auc_score(y_true, y_pred2)) / se
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return p

# DeLong comparisons: each component vs DSI
print("\n=== DeLong P-value vs DSI ===")
dsi_vals = df['DSI_mean'].values
for name in ['HR (mean 24h)', 'DBP (mean 24h)', 'SBP (mean 24h)', 'MAP (mean 24h)', 'SI (HR/SBP)', 'MSI (HR/MAP)', 'SOFA', 'Lactate']:
    vals = components[name]
    valid = pd.notna(vals) & pd.notna(dsi_vals)
    y_valid = y[valid]
    v1 = vals[valid]
    v2 = dsi_vals[valid]

    # For BP components, negate so higher = worse
    if name in ['DBP (mean 24h)', 'SBP (mean 24h)', 'MAP (mean 24h)']:
        v1 = -v1

    auc1 = roc_auc_score(y_valid, v1)
    auc2 = roc_auc_score(y_valid, v2)
    p = delong_test(y_valid, v1, v2)
    print(f"  {name} (AUC={auc1:.4f}) vs DSI (AUC={auc2:.4f}): DeLong P = {p:.4f}")
    results[f'{name}_vs_DSI_deLong_P'] = p

# Component matched analysis (Ospina-Tascón Fig 2/3 style)
# Partition into DBP quintiles, then within each DBP quintile, show mortality by DSI tertile
print("\n=== DBP-matched mortality by DSI tertile ===")
df['dbp_quintile'] = pd.qcut(df['DBP_mean'], 5, labels=['Q1(low)', 'Q2', 'Q3', 'Q4', 'Q5(high)'])
df['dsi_tertile'] = pd.qcut(df['DSI_mean'], 3, labels=['Low DSI', 'Mid DSI', 'High DSI'])

print(f"{'DBP Quintile':<12} {'DSI Tertile':<12} {'N':>6} {'Mortality %':>12}")
for dbp_q in ['Q1(low)', 'Q2', 'Q3', 'Q4', 'Q5(high)']:
    for dsi_t in ['Low DSI', 'Mid DSI', 'High DSI']:
        subset = df[(df['dbp_quintile'] == dbp_q) & (df['dsi_tertile'] == dsi_t)]
        n = len(subset)
        if n > 0:
            mort = subset['hospital_expire_flag'].mean() * 100
            print(f"{dbp_q:<12} {dsi_t:<12} {n:>6} {mort:>12.1f}%")

# HR-matched analysis
print("\n=== HR-matched mortality by DSI tertile ===")
df['hr_quintile'] = pd.qcut(df['HR_mean'], 5, labels=['Q1(low)', 'Q2', 'Q3', 'Q4', 'Q5(high)'])

print(f"{'HR Quintile':<12} {'DSI Tertile':<12} {'N':>6} {'Mortality %':>12}")
for hr_q in ['Q1(low)', 'Q2', 'Q3', 'Q4', 'Q5(high)']:
    for dsi_t in ['Low DSI', 'Mid DSI', 'High DSI']:
        subset = df[(df['hr_quintile'] == hr_q) & (df['dsi_tertile'] == dsi_t)]
        n = len(subset)
        if n > 0:
            mort = subset['hospital_expire_flag'].mean() * 100
            print(f"{hr_q:<12} {dsi_t:<12} {n:>6} {mort:>12.1f}%")

# Also compute: within each DBP quintile, DSI still predicts mortality (logistic regression)
print("\n=== Logistic regression: DSI predicting mortality within DBP quintiles ===")
from sklearn.linear_model import LogisticRegression
for dbp_q in ['Q1(low)', 'Q2', 'Q3', 'Q4', 'Q5(high)']:
    subset = df[df['dbp_quintile'] == dbp_q]
    if len(subset) < 50:
        continue
    X = subset[['DSI_mean']].values
    y_s = subset['hospital_expire_flag'].values
    if y_s.sum() < 5:
        continue
    lr = LogisticRegression(C=1e6, max_iter=1000)
    lr.fit(X, y_s)
    coef = lr.coef_[0][0]
    or_val = np.exp(coef)
    # Wald test
    from sklearn.utils import resample
    ors = []
    for _ in range(500):
        X_r, y_r = resample(X, y_s)
        if y_r.sum() < 2 or y_r.sum() > len(y_r) - 2:
            continue
        lr_r = LogisticRegression(C=1e6, max_iter=1000)
        lr_r.fit(X_r, y_r)
        ors.append(np.exp(lr_r.coef_[0][0]))
    ors = np.array(ors)
    ci_lo, ci_hi = np.percentile(ors, [2.5, 97.5])
    # P-value from Wald
    se = np.std(np.log(ors))
    if se > 0:
        z = coef / se
        p = 2 * (1 - stats.norm.cdf(abs(z)))
    else:
        p = 1.0
    print(f"  DBP {dbp_q}: DSI OR={or_val:.2f} (95% CI {ci_lo:.2f}-{ci_hi:.2f}), P={p:.4f}, N={len(subset)}")

# Save results
with open(f'{BASE}/component_decomposition_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\n=== Summary ===")
print(f"DSI AUC (unadjusted): {results['DSI (HR/DBP)']:.4f}")
print(f"HR AUC: {results['HR (mean 24h)']:.4f}")
print(f"DBP AUC: {results['DBP (mean 24h)']:.4f}")
print(f"SOFA AUC: {results['SOFA']:.4f}")
print(f"Lactate AUC: {results['Lactate']:.4f}")
print(f"DeLong DSI vs HR: P={results.get('HR (mean 24h)_vs_DSI_deLong_P', 'N/A')}")
print(f"DeLong DSI vs DBP: P={results.get('DBP (mean 24h)_vs_DSI_deLong_P', 'N/A')}")
print(f"DeLong DSI vs SOFA: P={results.get('SOFA_vs_DSI_deLong_P', 'N/A')}")
