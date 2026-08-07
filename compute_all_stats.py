import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score
from sklearn.utils import resample
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('analysis_dataset_revised.csv')
cc = df.copy()
y = cc['hospital_expire_flag'].values

print('='*60)
print('P0-1: BASELINE STATS (CC N=5728)')
print('='*60)
print(f'N = {len(cc)}')
print(f'Age: {cc["age_at_admission"].median():.0f} [{cc["age_at_admission"].quantile(0.25):.0f}-{cc["age_at_admission"].quantile(0.75):.0f}]')
print(f'Gender M: {(cc["gender"]=="M").sum()} ({(cc["gender"]=="M").mean()*100:.1f}%)')
print(f'ICU LOS: {cc["los"].median():.1f} [{cc["los"].quantile(0.25):.1f}-{cc["los"].quantile(0.75):.1f}]')
print(f'Lactate: {cc["lactate_first"].median():.1f} [{cc["lactate_first"].quantile(0.25):.1f}-{cc["lactate_first"].quantile(0.75):.1f}]')
print(f'WBC: {cc["wbc_first"].median():.1f} [{cc["wbc_first"].quantile(0.25):.1f}-{cc["wbc_first"].quantile(0.75):.1f}]')
print(f'Hb: {cc["hb_first"].median():.1f} [{cc["hb_first"].quantile(0.25):.1f}-{cc["hb_first"].quantile(0.75):.1f}]')
print(f'Cr: {cc["cr_first"].median():.1f} [{cc["cr_first"].quantile(0.25):.1f}-{cc["cr_first"].quantile(0.75):.1f}]')
print(f'CCI: {cc["CCI"].median():.0f} [{cc["CCI"].quantile(0.25):.0f}-{cc["CCI"].quantile(0.75):.0f}]')
print(f'SOFA: {cc["sofa"].median():.0f} [{cc["sofa"].quantile(0.25):.0f}-{cc["sofa"].quantile(0.75):.0f}]')
print(f'Mortality: {cc["hospital_expire_flag"].sum()}/{len(cc)} = {cc["hospital_expire_flag"].mean()*100:.1f}%')
print(f'ICU death strict: {cc["icu_death_strict"].sum()}')
print(f'Vasopressor: {cc["vasopressor_use"].sum()} ({cc["vasopressor_use"].mean()*100:.1f}%)')
print(f'MV: {cc["mechanical_ventilation"].sum()} ({cc["mechanical_ventilation"].mean()*100:.1f}%)')
print(f'Surgery: {cc["any_surgery"].sum()} ({cc["any_surgery"].mean()*100:.1f}%)')

for m in ['SI_mean','MSI_mean','DSI_mean','Age_SI_mean']:
    print(f'{m}: {cc[m].median():.2f} [{cc[m].quantile(0.25):.2f}-{cc[m].quantile(0.75):.2f}]')

# Subtype distribution
if 'subtype' in cc.columns:
    print(f'Subtypes: {cc["subtype"].value_counts().to_dict()}')

print()
print('='*60)
print('P0-2: BASIC BASELINE AUC')
print('='*60)
X_b = cc[['age_at_admission','gender','CCI']].copy()
X_b['gender'] = (X_b['gender']=='M').astype(int)
X_b = sm.add_constant(X_b)
m_b = sm.Logit(y, X_b).fit(disp=0)
auc_b = roc_auc_score(y, m_b.predict(X_b))
print(f'Age+Sex+CCI AUC = {auc_b:.4f}')

print()
print('='*60)
print('P0-7: DeLong TEST')
print('='*60)
X_e = cc[['age_at_admission','gender','CCI','lactate_first','wbc_first','vasopressor_use','any_surgery','mechanical_ventilation','sofa']].copy()
X_e['gender'] = (X_e['gender']=='M').astype(int)
X_e = sm.add_constant(X_e)
m_e = sm.Logit(y, X_e).fit(disp=0)
pred_e = m_e.predict(X_e)
auc_e = roc_auc_score(y, pred_e)

X_d = X_e.copy()
X_d['DSI'] = cc['DSI_mean'].values
m_d = sm.Logit(y, X_d).fit(disp=0)
pred_d = m_d.predict(X_d)
auc_d = roc_auc_score(y, pred_d)

print(f'Extended AUC = {auc_e:.4f}')
print(f'Extended+DSI AUC = {auc_d:.4f}')
print(f'DeltaAUC = {auc_d-auc_e:.4f}')

# DeLong test
cases = np.where(y == 1)[0]
controls = np.where(y == 0)[0]
n1 = len(cases)
n0 = len(controls)

pe = pred_e.values
pd_arr = pred_d.values

V10_1 = pe[cases]
V01_1 = pe[controls]
V10_2 = pd_arr[cases]
V01_2 = pd_arr[controls]

S01_1 = np.array([np.mean(V10_1 > v) + 0.5*np.mean(V10_1 == v) for v in V01_1])
S10_1 = np.array([np.mean(V01_1 < v) + 0.5*np.mean(V01_1 == v) for v in V10_1])
S01_2 = np.array([np.mean(V10_2 > v) + 0.5*np.mean(V10_2 == v) for v in V01_2])
S10_2 = np.array([np.mean(V01_2 < v) + 0.5*np.mean(V01_2 == v) for v in V10_2])

S01_cov = np.cov(np.column_stack([S01_1, S01_2]), rowvar=False)
S10_cov = np.cov(np.column_stack([S10_1, S10_2]), rowvar=False)
cov = S01_cov / n0 + S10_cov / n1
var_diff = cov[0,0] + cov[1,1] - 2*cov[0,1]

if var_diff > 0:
    z_delong = (auc_d - auc_e) / np.sqrt(var_diff)
    p_delong = 2 * (1 - stats.norm.cdf(abs(z_delong)))
    print(f'DeLong z = {z_delong:.4f}, P = {p_delong:.6f}')
else:
    print('var_diff <= 0, cannot compute DeLong')

print()
print('='*60)
print('P0-8: VIF')
print('='*60)
X_vif = cc[['age_at_admission','gender','CCI','lactate_first','wbc_first','vasopressor_use','any_surgery','mechanical_ventilation','sofa']].copy()
X_vif['gender'] = (X_vif['gender']=='M').astype(int)
X_vif = sm.add_constant(X_vif)
print('Extended model VIF:')
for i, col in enumerate(X_vif.columns):
    if col == 'const':
        continue
    vif = variance_inflation_factor(X_vif.values, i)
    print(f'  {col}: VIF={vif:.2f}')

X_vif2 = X_vif.copy()
X_vif2['DSI'] = cc['DSI_mean'].values
print('Extended+DSI model VIF:')
for i, col in enumerate(X_vif2.columns):
    if col == 'const':
        continue
    vif = variance_inflation_factor(X_vif2.values, i)
    print(f'  {col}: VIF={vif:.2f}')

X_vif3 = X_vif.copy()
X_vif3['SI'] = cc['SI_mean'].values
X_vif3['MSI'] = cc['MSI_mean'].values
X_vif3['DSI'] = cc['DSI_mean'].values
X_vif3['Age_SI'] = cc['Age_SI_mean'].values
print('Extended+allSI model VIF:')
for i, col in enumerate(X_vif3.columns):
    if col == 'const':
        continue
    vif = variance_inflation_factor(X_vif3.values, i)
    print(f'  {col}: VIF={vif:.2f}')

print()
print('='*60)
print('TABLE 4: RCS (recomputed with v5 data)')
print('='*60)
# RCS with 4 knots (5th, 35th, 65th, 95th percentiles)
def rcs_transform(x, knots):
    k = len(knots)
    t = np.zeros((len(x), k-1))
    t[:,0] = x - knots[0]
    for j in range(1, k-1):
        t[:,j] = (x - knots[j])**3 - (x - knots[k-2])**3 * (knots[k-1] - knots[j]) / (knots[k-1] - knots[k-2])
        t[:,j] += (x - knots[k-1])**3 * (knots[k-2] - knots[j]) / (knots[k-1] - knots[k-2])
    return t

for metric in ['SI_mean','MSI_mean','DSI_mean','Age_SI_mean']:
    x = cc[metric].values
    knots = np.percentile(x, [5, 35, 65, 95])
    t = rcs_transform(x, knots)
    X_rcs = cc[['age_at_admission','gender','CCI']].copy()
    X_rcs['gender'] = (X_rcs['gender']=='M').astype(int)
    X_rcs = sm.add_constant(X_rcs)
    X_rcs['rcs1'] = t[:,0]
    X_rcs['rcs2'] = t[:,1]
    X_rcs['rcs3'] = t[:,2]
    try:
        m_rcs = sm.Logit(y, X_rcs).fit(disp=0)
        # Overall: LR test of rcs1,rcs2,rcs3 = 0
        lr_full = m_rcs.llf
        X_null = cc[['age_at_admission','gender','CCI']].copy()
        X_null['gender'] = (X_null['gender']=='M').astype(int)
        X_null = sm.add_constant(X_null)
        m_null = sm.Logit(y, X_null).fit(disp=0)
        lr_null = m_null.llf
        lr_stat = -2 * (lr_null - lr_full)
        p_overall = 1 - stats.chi2.cdf(lr_stat, 3)
        # Nonlinear: test rcs2=rcs3=0 (linear = rcs1 only)
        # Wald test for rcs2, rcs3
        R = np.zeros((2, len(m_rcs.params)))
        r_idx = list(m_rcs.params.index)
        rcs2_idx = r_idx.index('rcs2')
        rcs3_idx = r_idx.index('rcs3')
        R[0, rcs2_idx] = 1
        R[1, rcs3_idx] = 1
        wald = m_rcs.wald_test(R)
        p_nonlinear = float(wald.pvalue)
        print(f'{metric}: P_overall={p_overall:.2e}, P_nonlinear={p_nonlinear:.3f}, knots=[{knots[0]:.2f}, {knots[1]:.2f}, {knots[2]:.2f}, {knots[3]:.2f}]')
    except Exception as e:
        print(f'{metric}: Error - {e}')

print()
print('='*60)
print('TABLE 5: KM LOG-RANK (recomputed)')
print('='*60)
from lifelines.statistics import logrank_test
cc['dsi_q'] = pd.qcut(cc['DSI_mean'], 4, labels=['Q1','Q2','Q3','Q4'])

# Use hospital LOS as time axis
if 'hosp_los_days' in cc.columns:
    time_col = 'hosp_los_days'
elif 'hospital_los' in cc.columns:
    time_col = 'hospital_los'
else:
    time_col = 'los'  # ICU LOS as proxy
    print(f'WARNING: Using {time_col} as time axis (no hospital LOS found)')

event = cc['hospital_expire_flag'].values
time = cc[time_col].values

# Pairwise log-rank across 4 quartiles
groups = cc['dsi_q'].values
q_labels = ['Q1','Q2','Q3','Q4']
# Overall log-rank (multi-group)
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()

# Multi-group log-rank
mask = ~np.isnan(time)
t = time[mask]
e = event[mask]
g = groups[mask]

result_pairs = []
for i in range(4):
    for j in range(i+1, 4):
        mask_i = g == q_labels[i]
        mask_j = g == q_labels[j]
        if mask_i.sum() > 0 and mask_j.sum() > 0:
            lr = logrank_test(t[mask_i], t[mask_j], e[mask_i], e[mask_j])
            result_pairs.append(f'{q_labels[i]} vs {q_labels[j]}: P={lr.p_value:.2e}')

# Overall chi2
from lifelines.statistics import multivariate_logrank_test
mlr = multivariate_logrank_test(t, g, e)
print(f'Overall log-rank: chi2={mlr.test_statistic:.2f}, P={mlr.p_value:.2e}')
for p in result_pairs:
    print(f'  {p}')

print()
print('='*60)
print('TABLE 6: CALIBRATION (recomputed with v5 models)')
print('='*60)
# 4 models: basic, extended, extended+DSI, extended+allSI
from sklearn.calibration import calibration_curve

models_cal = {
    'Basic baseline': (m_b, X_b),
    'Extended baseline': (m_e, X_e),
    'Extended + DSI': (m_d, X_d),
}

X_all = X_e.copy()
X_all['SI'] = cc['SI_mean'].values
X_all['MSI'] = cc['MSI_mean'].values
X_all['DSI'] = cc['DSI_mean'].values
X_all['Age_SI'] = cc['Age_SI_mean'].values
m_all = sm.Logit(y, X_all).fit(disp=0)
models_cal['Extended + all SI'] = (m_all, X_all)

for name, (model, X) in models_cal.items():
    pred = model.predict(X)
    brier = np.mean((pred - y)**2)
    # HL test (10 groups)
    groups_hl = pd.qcut(pred, 10, duplicates='drop')
    obs = pd.DataFrame({'y': y, 'pred': pred, 'group': groups_hl}).groupby('group')
    obs_events = obs['y'].sum()
    exp_events = obs['pred'].sum()
    obs_n = obs['y'].count()
    hl = np.sum((obs_events - exp_events)**2 / (exp_events * (1 - exp_events/obs_n) + 0.001))
    hl_p = 1 - stats.chi2.cdf(hl, len(obs_events)-2)
    print(f'{name}: Brier={brier:.4f}, HL chi2={hl:.2f}, HL P={hl_p:.3f}')

print()
print('='*60)
print('TABLE 7: FOREST PLOT (Extended+DSI model coefficients)')
print('='*60)
print(f'{"Variable":<25} {"OR":>8} {"CI_lower":>10} {"CI_upper":>10} {"P":>12}')
for var in m_d.params.index:
    if var == 'const':
        continue
    or_val = np.exp(m_d.params[var])
    ci_lower = np.exp(m_d.conf_int().loc[var, 0])
    ci_upper = np.exp(m_d.conf_int().loc[var, 1])
    p_val = m_d.pvalues[var]
    print(f'{var:<25} {or_val:>8.3f} {ci_lower:>10.3f} {ci_upper:>10.3f} {p_val:>12.2e}')

print()
print('='*60)
print('TABLE 8: SUBGROUP AUC (Extended+DSI by subtype)')
print('='*60)
if 'subtype' in cc.columns:
    for sub in cc['subtype'].unique():
        sub_cc = cc[cc['subtype']==sub]
        if len(sub_cc) < 50 or sub_cc['hospital_expire_flag'].nunique() < 2:
            print(f'{sub}: N={len(sub_cc)}, skipped (too small)')
            continue
        y_sub = sub_cc['hospital_expire_flag'].values
        X_sub = sub_cc[['age_at_admission','gender','CCI','lactate_first','wbc_first','vasopressor_use','any_surgery','mechanical_ventilation','sofa','DSI_mean']].copy()
        X_sub['gender'] = (X_sub['gender']=='M').astype(int)
        X_sub = sm.add_constant(X_sub)
        try:
            # Drop any_surgery if all same value within subgroup
            for col in ['any_surgery','vasopressor_use','mechanical_ventilation']:
                if X_sub[col].nunique() < 2:
                    X_sub = X_sub.drop(columns=[col])
            m_sub = sm.Logit(y_sub, X_sub).fit(disp=0)
            auc_sub = roc_auc_score(y_sub, m_sub.predict(X_sub))
            print(f'{sub}: N={len(sub_cc)}, deaths={y_sub.sum()}, AUC={auc_sub:.3f}')
        except Exception as e:
            # Use extended model predictions
            X_sub_e = sub_cc[['age_at_admission','gender','CCI','lactate_first','wbc_first','vasopressor_use','any_surgery','mechanical_ventilation','sofa','DSI_mean']].copy()
            X_sub_e['gender'] = (X_sub_e['gender']=='M').astype(int)
            X_sub_e = sm.add_constant(X_sub_e)
            # Use the full model coefficients
            pred_sub = m_d.predict(X_sub_e[m_d.params.index])
            auc_sub = roc_auc_score(y_sub, pred_sub)
            print(f'{sub}: N={len(sub_cc)}, deaths={y_sub.sum()}, AUC={auc_sub:.3f} (full model applied)')
else:
    print('No subtype column found')

# Surgical vs non-surgical
for surg_label, surg_val in [('Surgical', 1), ('Non-surgical', 0)]:
    sub_cc = cc[cc['any_surgery']==surg_val]
    y_sub = sub_cc['hospital_expire_flag'].values
    X_sub = sub_cc[['age_at_admission','gender','CCI','lactate_first','wbc_first','vasopressor_use','mechanical_ventilation','sofa','DSI_mean']].copy()
    X_sub['gender'] = (X_sub['gender']=='M').astype(int)
    X_sub = sm.add_constant(X_sub)
    try:
        m_sub = sm.Logit(y_sub, X_sub).fit(disp=0)
        auc_sub = roc_auc_score(y_sub, m_sub.predict(X_sub))
        dsi_or = np.exp(m_sub.params.get('DSI_mean', 0))
        dsi_p = m_sub.pvalues.get('DSI_mean', 1)
        print(f'{surg_label}: N={len(sub_cc)}, deaths={y_sub.sum()}, AUC={auc_sub:.3f}, DSI OR={dsi_or:.2f}, P={dsi_p:.2e}')
    except Exception as e:
        print(f'{surg_label}: N={len(sub_cc)}, Error: {e}')

print()
print('='*60)
print('TABLE S3: BASELINE BY DSI QUARTILE (with SOFA)')
print('='*60)
for q_label in ['Q1','Q2','Q3','Q4']:
    sub = cc[cc['dsi_q']==q_label]
    print(f'{q_label} (N={len(sub)}):')
    print(f'  Age: {sub["age_at_admission"].median():.0f} [{sub["age_at_admission"].quantile(0.25):.0f}-{sub["age_at_admission"].quantile(0.75):.0f}]')
    print(f'  Male: {(sub["gender"]=="M").sum()} ({(sub["gender"]=="M").mean()*100:.1f}%)')
    print(f'  SOFA: {sub["sofa"].median():.0f} [{sub["sofa"].quantile(0.25):.0f}-{sub["sofa"].quantile(0.75):.0f}]')
    print(f'  CCI: {sub["CCI"].median():.0f} [{sub["CCI"].quantile(0.25):.0f}-{sub["CCI"].quantile(0.75):.0f}]')
    print(f'  Lactate: {sub["lactate_first"].median():.1f} [{sub["lactate_first"].quantile(0.25):.1f}-{sub["lactate_first"].quantile(0.75):.1f}]')
    print(f'  WBC: {sub["wbc_first"].median():.1f} [{sub["wbc_first"].quantile(0.25):.1f}-{sub["wbc_first"].quantile(0.75):.1f}]')
    print(f'  ICU LOS: {sub["los"].median():.1f} [{sub["los"].quantile(0.25):.1f}-{sub["los"].quantile(0.75):.1f}]')
    print(f'  Vasopressor: {sub["vasopressor_use"].sum()} ({sub["vasopressor_use"].mean()*100:.1f}%)')
    print(f'  MV: {sub["mechanical_ventilation"].sum()} ({sub["mechanical_ventilation"].mean()*100:.1f}%)')
    print(f'  Surgery: {sub["any_surgery"].sum()} ({sub["any_surgery"].mean()*100:.1f}%)')
    print(f'  Mortality: {sub["hospital_expire_flag"].sum()} ({sub["hospital_expire_flag"].mean()*100:.1f}%)')
    print(f'  ICU death: {sub["icu_death_strict"].sum()} ({sub["icu_death_strict"].mean()*100:.1f}%)')

print()
print('='*60)
print('AUC 95% CI (bootstrap, 500 resamples)')
print('='*60)
n_boot = 500
for name, model, X in [('Basic', m_b, X_b), ('Extended', m_e, X_e), ('Extended+DSI', m_d, X_d)]:
    aucs = []
    for i in range(n_boot):
        idx = resample(range(len(y)), n_samples=len(y), random_state=i)
        yb = y[idx]
        pb = model.predict(X).values[idx]
        if len(np.unique(yb)) < 2:
            continue
        try:
            aucs.append(roc_auc_score(yb, pb))
        except:
            continue
    aucs = np.array(aucs)
    auc_val = roc_auc_score(y, model.predict(X))
    print(f'{name}: AUC={auc_val:.3f} (95% CI: {np.percentile(aucs,2.5):.3f}-{np.percentile(aucs,97.5):.3f})')

# Extended+allSI
aucs = []
for i in range(n_boot):
    idx = resample(range(len(y)), n_samples=len(y), random_state=i)
    yb = y[idx]
    pb = m_all.predict(X_all).values[idx]
    if len(np.unique(yb)) < 2:
        continue
    try:
        aucs.append(roc_auc_score(yb, pb))
    except:
        continue
aucs = np.array(aucs)
auc_val = roc_auc_score(y, m_all.predict(X_all))
print(f'Extended+allSI: AUC={auc_val:.3f} (95% CI: {np.percentile(aucs,2.5):.3f}-{np.percentile(aucs,97.5):.3f})')

print()
print('='*60)
print('SOFA non-survivors vs survivors')
print('='*60)
non_surv = cc[cc['hospital_expire_flag']==1]
surv = cc[cc['hospital_expire_flag']==0]
print(f'SOFA non-survivors: {non_surv["sofa"].median():.0f} [{non_surv["sofa"].quantile(0.25):.0f}-{non_surv["sofa"].quantile(0.75):.0f}]')
print(f'SOFA survivors: {surv["sofa"].median():.0f} [{surv["sofa"].quantile(0.25):.0f}-{surv["sofa"].quantile(0.75):.0f}]')
u_stat, u_p = stats.mannwhitneyu(non_surv['sofa'], surv['sofa'], alternative='two-sided')
print(f'Mann-Whitney U P={u_p:.2e}')

# Surgery <=24h
if 'surgery_24h' in cc.columns:
    print(f'Surgery <=24h: {cc["surgery_24h"].sum()} ({cc["surgery_24h"].mean()*100:.1f}%)')

print()
print('DONE')
