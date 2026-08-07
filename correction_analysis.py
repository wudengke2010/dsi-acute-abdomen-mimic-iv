"""
Comprehensive correction analysis script for SCI paper v4
- Uses corrected dataset with proper icu_death_strict and hospital_expire_flag
- Primary outcome: in-hospital mortality (hospital_expire_flag)
- Secondary outcome: strict ICU mortality (icu_death_strict)
- All CC analyses use 5,728 complete cases consistently
- All descriptive statistics use CC dataset (not full 8,933)
"""

import pandas as pd, numpy as np, os
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve
import warnings
warnings.filterwarnings('ignore')

# Load corrected dataset
df = pd.read_csv('analysis_dataset_corrected.csv')
print(f"Total dataset: {len(df)} rows")

# Define variables
df['gender_male'] = (df['gender'] == 'M').astype(int)

model_vars_base = ['age_at_admission', 'gender_male', 'CCI']
model_vars_ext = ['lactate_first', 'wbc_first', 'vasopressor_use', 'any_surgery', 'mechanical_ventilation']
si_vars = ['SI_mean', 'MSI_mean', 'DSI_mean', 'Age_SI_mean']

# Primary outcome: hospital_expire_flag (in-hospital mortality)
y_col = 'hospital_expire_flag'

# Complete case analysis
required = model_vars_base + model_vars_ext + si_vars + [y_col]
df_cc = df[required].dropna().copy()
print(f"Complete cases: {len(df_cc)}")

# Also add icu_death_strict for secondary analysis
df_cc['icu_death_strict'] = df.loc[df_cc.index, 'icu_death_strict']
df_cc['abdomen_subtype'] = df.loc[df_cc.index, 'abdomen_subtype']

# ============================================================
# 1. CC Descriptive Statistics (Section 3.1)
# ============================================================
print("\n=== 1. CC Descriptive Statistics ===")
print(f"N: {len(df_cc)}")
print(f"In-hospital mortality: {df_cc[y_col].mean()*100:.1f}% ({df_cc[y_col].sum()} deaths)")
print(f"Strict ICU mortality: {df_cc['icu_death_strict'].mean()*100:.1f}% ({df_cc['icu_death_strict'].sum()} deaths)")
print(f"Mean age: {df_cc['age_at_admission'].mean():.1f}")
print(f"Age IQR: {df_cc['age_at_admission'].quantile(0.25):.0f}-{df_cc['age_at_admission'].quantile(0.75):.0f}")
print(f"Male: {df_cc['gender_male'].mean()*100:.1f}%")
print(f"CCI median: {df_cc['CCI'].median():.0f}")
print(f"Lactate median: {df_cc['lactate_first'].median():.1f}")
print(f"WBC median: {df_cc['wbc_first'].median():.1f}")
print(f"Vasopressor: {df_cc['vasopressor_use'].mean()*100:.1f}%")
print(f"MV: {df_cc['mechanical_ventilation'].mean()*100:.1f}%")
print(f"Surgery: {df_cc['any_surgery'].mean()*100:.1f}%")

# Death breakdown
hosp_dead = df_cc[y_col] == 1
icu_dead = df_cc['icu_death_strict'] == 1
icu_alive_hosp_dead = (icu_dead == 0) & (hosp_dead == 1)
print(f"Died during ICU stay: {icu_dead.sum()} ({icu_dead.sum()/hosp_dead.sum()*100:.1f}% of hospital deaths)")
print(f"Survived ICU but died in hospital: {icu_alive_hosp_dead.sum()} ({icu_alive_hosp_dead.sum()/hosp_dead.sum()*100:.1f}% of hospital deaths)")

# ============================================================
# 2. Subtype Distribution in CC
# ============================================================
print("\n=== 2. Subtype Distribution (CC) ===")
subtype_counts = df_cc['abdomen_subtype'].value_counts()
for st, cnt in subtype_counts.items():
    pct = cnt/len(df_cc)*100
    hosp_death = df_cc[df_cc['abdomen_subtype']==st][y_col].mean()*100
    icu_death = df_cc[df_cc['abdomen_subtype']==st]['icu_death_strict'].mean()*100
    print(f"{st}: n={cnt} ({pct:.1f}%), hospital mortality={hosp_death:.1f}%, ICU mortality={icu_death:.1f}%")

# ============================================================
# 3. DSI Quartile in CC (Section 3.2)
# ============================================================
print("\n=== 3. DSI Quartile (CC 5,728) ===")
df_cc['DSI_quartile'] = pd.qcut(df_cc['DSI_mean'], q=4, labels=['Q1','Q2','Q3','Q4'])

quartile_stats = []
for q in ['Q1','Q2','Q3','Q4']:
    qd = df_cc[df_cc['DSI_quartile']==q]
    hosp_mort = qd[y_col].mean()*100
    icu_mort = qd['icu_death_strict'].mean()*100
    n = len(qd)
    hosp_deaths = qd[y_col].sum()
    lac_med = qd['lactate_first'].median()
    vaso_pct = qd['vasopressor_use'].mean()*100
    surg_pct = qd['any_surgery'].mean()*100
    mv_pct = qd['mechanical_ventilation'].mean()*100
    print(f"{q}: N={n}, Hospital mortality={hosp_mort:.1f}%({hosp_deaths}), ICU mortality={icu_mort:.1f}%, Lac={lac_med:.1f}, Vaso={vaso_pct:.1f}%, Surgery={surg_pct:.1f}%, MV={mv_pct:.1f}%")
    quartile_stats.append({
        'Quartile': q, 'N': n, 
        'Hospital_death_pct': hosp_mort, 'Hospital_death_n': hosp_deaths,
        'ICU_death_pct': icu_mort,
        'Lactate_median': lac_med, 'Vasopressor_pct': vaso_pct,
        'Surgery_pct': surg_pct, 'MV_pct': mv_pct
    })

pd.DataFrame(quartile_stats).to_csv('table_DSI_quartile_corrected.csv', index=False)

# Chi-square test for quartile mortality gradient
q1_death = df_cc[df_cc['DSI_quartile']=='Q1'][y_col].sum()
q2_death = df_cc[df_cc['DSI_quartile']=='Q2'][y_col].sum()
q3_death = df_cc[df_cc['DSI_quartile']=='Q3'][y_col].sum()
q4_death = df_cc[df_cc['DSI_quartile']=='Q4'][y_col].sum()
q1_n = len(df_cc[df_cc['DSI_quartile']=='Q1'])
q2_n = len(df_cc[df_cc['DSI_quartile']=='Q2'])
q3_n = len(df_cc[df_cc['DSI_quartile']=='Q3'])
q4_n = len(df_cc[df_cc['DSI_quartile']=='Q4'])
chi2, p_val = stats.chi2_contingency([[q1_death, q1_n-q1_death],[q2_death, q2_n-q2_death],[q3_death, q3_n-q3_death],[q4_death, q4_n-q4_death]])[:2]
print(f"Chi-square: {chi2:.2f}, P={p_val:.2e}")

# ============================================================
# 4. Logistic Regression Models on CC
# ============================================================
print("\n=== 4. Logistic Regression Models (CC 5,728) ===")
import statsmodels.api as sm

y = df_cc[y_col]

# Basic baseline
X_basic = df_cc[model_vars_base]
model_basic = sm.Logit(y, sm.add_constant(X_basic)).fit(disp=0)
auc_basic = roc_auc_score(y, model_basic.predict(sm.add_constant(X_basic)))
print(f"Basic baseline AUC: {auc_basic:.4f}")

# Extended baseline
X_ext = df_cc[model_vars_base + model_vars_ext]
model_ext = sm.Logit(y, sm.add_constant(X_ext)).fit(disp=0)
auc_ext = roc_auc_score(y, model_ext.predict(sm.add_constant(X_ext)))
print(f"Extended baseline AUC: {auc_ext:.4f}")

# Extended + DSI
X_dsi = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']]
model_dsi = sm.Logit(y, sm.add_constant(X_dsi)).fit(disp=0)
auc_dsi = roc_auc_score(y, model_dsi.predict(sm.add_constant(X_dsi)))
print(f"Extended+DSI AUC: {auc_dsi:.4f}")

# Extended + all SI derivatives
X_all = df_cc[model_vars_base + model_vars_ext + si_vars]
model_all = sm.Logit(y, sm.add_constant(X_all)).fit(disp=0)
auc_all = roc_auc_score(y, model_all.predict(sm.add_constant(X_all)))
print(f"Extended+all SI AUC: {auc_all:.4f}")

# ============================================================
# 5. NRI/IDI Calculation (binary at 50% threshold)
# ============================================================
print("\n=== 5. NRI/IDI (Binary, threshold=50%) ===")
y_pred_ext = model_ext.predict(sm.add_constant(X_ext))
y_pred_dsi = model_dsi.predict(sm.add_constant(X_dsi))

threshold = 0.5
events = y == 1
non_events = y == 0

# NRI
ext_class = (y_pred_ext >= threshold).astype(int)
dsi_class = (y_pred_dsi >= threshold).astype(int)

# NRI events
reclassified_events_up = ((ext_class == 0) & (dsi_class == 1) & events).sum()
reclassified_events_down = ((ext_class == 1) & (dsi_class == 0) & events).sum()
nri_events = (reclassified_events_up - reclassified_events_down) / events.sum()

# NRI non-events
reclassified_non_up = ((ext_class == 0) & (dsi_class == 1) & non_events).sum()
reclassified_non_down = ((ext_class == 1) & (dsi_class == 0) & non_events).sum()
nri_non_events = -(reclassified_non_up - reclassified_non_down) / non_events.sum()

nri_total = nri_events + nri_non_events
print(f"NRI_events: {nri_events:.4f}")
print(f"NRI_non_events: {nri_non_events:.4f}")
print(f"NRI_total: {nri_total:.4f}")

# IDI
idi = (y_pred_dsi[events].mean() - y_pred_ext[events].mean()) - (y_pred_dsi[non_events].mean() - y_pred_ext[non_events].mean())
isi = y_pred_dsi[events].mean() - y_pred_ext[events].mean()
ipi = y_pred_dsi[non_events].mean() - y_pred_ext[non_events].mean()
idi = isi - ipi

# Z-test for IDI
se_idi = np.sqrt(np.var(y_pred_dsi[events] - y_pred_ext[events])/events.sum() + 
                  np.var(y_pred_dsi[non_events] - y_pred_ext[non_events])/non_events.sum())
z_idi = idi / se_idi
p_idi = 2 * (1 - stats.norm.cdf(abs(z_idi)))
print(f"IDI: {idi:.4f}")
print(f"ISI: {isi:.4f}")
print(f"IPI: {ipi:.4f}")
print(f"Z-test: {z_idi:.2f}")
print(f"P: {p_idi:.2e}")

# ============================================================
# 6. Bootstrap Internal Validation (1000 resamples)
# ============================================================
print("\n=== 6. Bootstrap Validation ===")
np.random.seed(42)
n_boot = 1000
optimism_basic = []
optimism_ext = []
optimism_dsi = []
optimism_all = []

for i in range(n_boot):
    idx_boot = np.random.choice(len(df_cc), len(df_cc), replace=True)
    df_boot = df_cc.iloc[idx_boot]
    y_boot = df_boot[y_col]
    
    try:
        # Basic baseline
        X_b = df_boot[model_vars_base]
        m_b = sm.Logit(y_boot, sm.add_constant(X_b)).fit(disp=0, maxiter=100)
        auc_b_boot = roc_auc_score(y_boot, m_b.predict(sm.add_constant(X_b)))
        auc_b_orig = roc_auc_score(y, m_b.predict(sm.add_constant(df_cc[model_vars_base])))
        optimism_basic.append(auc_b_boot - auc_b_orig)
        
        # Extended baseline
        X_e = df_boot[model_vars_base + model_vars_ext]
        m_e = sm.Logit(y_boot, sm.add_constant(X_e)).fit(disp=0, maxiter=100)
        auc_e_boot = roc_auc_score(y_boot, m_e.predict(sm.add_constant(X_e)))
        auc_e_orig = roc_auc_score(y, m_e.predict(sm.add_constant(df_cc[model_vars_base + model_vars_ext])))
        optimism_ext.append(auc_e_boot - auc_e_orig)
        
        # Extended+DSI
        X_d = df_boot[model_vars_base + model_vars_ext + ['DSI_mean']]
        m_d = sm.Logit(y_boot, sm.add_constant(X_d)).fit(disp=0, maxiter=100)
        auc_d_boot = roc_auc_score(y_boot, m_d.predict(sm.add_constant(X_d)))
        auc_d_orig = roc_auc_score(y, m_d.predict(sm.add_constant(df_cc[model_vars_base + model_vars_ext + ['DSI_mean']])))
        optimism_dsi.append(auc_d_boot - auc_d_orig)
        
        # Extended+all SI
        X_a = df_boot[model_vars_base + model_vars_ext + si_vars]
        m_a = sm.Logit(y_boot, sm.add_constant(X_a)).fit(disp=0, maxiter=100)
        auc_a_boot = roc_auc_score(y_boot, m_a.predict(sm.add_constant(X_a)))
        auc_a_orig = roc_auc_score(y, m_a.predict(sm.add_constant(df_cc[model_vars_base + model_vars_ext + si_vars])))
        optimism_all.append(auc_a_boot - auc_a_orig)
    except:
        continue

print(f"Bootstrap iterations completed: {len(optimism_basic)}")
optimism_mean_basic = np.mean(optimism_basic)
optimism_mean_ext = np.mean(optimism_ext)
optimism_mean_dsi = np.mean(optimism_dsi)
optimism_mean_all = np.mean(optimism_all)

print(f"Basic: AUC={auc_basic:.4f}, optimism={optimism_mean_basic:.4f}, corrected={auc_basic-optimism_mean_basic:.4f}")
print(f"Extended: AUC={auc_ext:.4f}, optimism={optimism_mean_ext:.4f}, corrected={auc_ext-optimism_mean_ext:.4f}")
print(f"Extended+DSI: AUC={auc_dsi:.4f}, optimism={optimism_mean_dsi:.4f}, corrected={auc_dsi-optimism_mean_dsi:.4f}")
print(f"Extended+all SI: AUC={auc_all:.4f}, optimism={optimism_mean_all:.4f}, corrected={auc_all-optimism_mean_all:.4f}")

# ============================================================
# 7. Sensitivity Analyses
# ============================================================
print("\n=== 7. Sensitivity Analyses ===")

# 7a. Exclude LOS<24h
df_24h = df[df['los'] >= 1].copy()
df_24h['gender_male'] = (df_24h['gender'] == 'M').astype(int)
df_24h_cc = df_24h[required].dropna()
df_24h_cc[y_col] = df_24h.loc[df_24h_cc.index, y_col]
y_24h = df_24h_cc[y_col]
X_24h = df_24h[model_vars_base + model_vars_ext + ['DSI_mean']]
try:
    m_24h = sm.Logit(y_24h, sm.add_constant(X_24h)).fit(disp=0)
    auc_24h = roc_auc_score(y_24h, m_24h.predict(sm.add_constant(X_24h)))
    print(f"Exclude LOS<24h: N={len(df_24h_cc)}, AUC={auc_24h:.3f}")
except Exception as e:
    print(f"Exclude LOS<24h: Error {e}")

# 7b. Non-surgical
df_nosurg = df[df['any_surgery'] == 0].copy()
df_nosurg['gender_male'] = (df_nosurg['gender'] == 'M').astype(int)
nosurg_vars = model_vars_base + ['lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'DSI_mean', y_col]
df_nosurg_cc = df_nosurg[nosurg_vars].dropna()
y_nosurg = df_nosurg_cc[y_col]
X_nosurg = df_nosurg_cc[model_vars_base + ['lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'DSI_mean']]
try:
    m_nosurg = sm.Logit(y_nosurg, sm.add_constant(X_nosurg)).fit(disp=0)
    auc_nosurg = roc_auc_score(y_nosurg, m_nosurg.predict(sm.add_constant(X_nosurg)))
    print(f"Non-surgical: N={len(df_nosurg_cc)}, AUC={auc_nosurg:.3f}")
except Exception as e:
    print(f"Non-surgical: Error {e}")

# 7c. Surgical
df_surg = df[df['any_surgery'] == 1].copy()
df_surg['gender_male'] = (df_surg['gender'] == 'M').astype(int)
df_surg_cc = df_surg[nosurg_vars].dropna()
y_surg = df_surg_cc[y_col]
X_surg = df_surg_cc[model_vars_base + ['lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'DSI_mean']]
try:
    m_surg = sm.Logit(y_surg, sm.add_constant(X_surg)).fit(disp=0)
    auc_surg = roc_auc_score(y_surg, m_surg.predict(sm.add_constant(X_surg)))
    print(f"Surgical: N={len(df_surg_cc)}, AUC={auc_surg:.3f}")
except Exception as e:
    print(f"Surgical: Error {e}")

# 7d. Subtype-specific
for subtype in ['inflammation', 'obstruction', 'perforation', 'ischemia']:
    sub_df = df[df['abdomen_subtype'] == subtype].copy()
    sub_df['gender_male'] = (sub_df['gender'] == 'M').astype(int)
    sub_vars = model_vars_base + ['lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'DSI_mean', y_col]
    sub_cc = sub_df[sub_vars].dropna()
    if len(sub_cc) > 50:
        y_sub = sub_cc[y_col]
        X_sub = sub_cc[model_vars_base + ['lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'DSI_mean']]
        try:
            m_sub = sm.Logit(y_sub, sm.add_constant(X_sub)).fit(disp=0)
            auc_sub = roc_auc_score(y_sub, m_sub.predict(sm.add_constant(X_sub)))
            hosp_mort = y_sub.mean()*100
            print(f"{subtype}: N={len(sub_cc)}, AUC={auc_sub:.3f}, hospital mortality={hosp_mort:.1f}%")
        except Exception as e:
            print(f"{subtype}: N={len(sub_cc)}, Error {e}")
    else:
        print(f"{subtype}: N={len(sub_cc)}, too small for model")

# 7e. Different time windows
for si_time in ['first', 'max', 'mean']:
    var = f'DSI_{si_time}'
    if var in df.columns:
        tw_vars = model_vars_base + model_vars_ext + [var, y_col]
        tw_cc = df[tw_vars].dropna()
        if len(tw_cc) > 50:
            y_tw = tw_cc[y_col]
            X_tw = tw_cc[model_vars_base + model_vars_ext + [var]]
            try:
                m_tw = sm.Logit(y_tw, sm.add_constant(X_tw)).fit(disp=0)
                auc_tw = roc_auc_score(y_tw, m_tw.predict(sm.add_constant(X_tw)))
                print(f"DSI_{si_time}: N={len(tw_cc)}, AUC={auc_tw:.3f}")
            except Exception as e:
                print(f"DSI_{si_time}: Error {e}")

# ============================================================
# 8. Full model coefficients (for forest plot)
# ============================================================
print("\n=== 8. Full Model Coefficients ===")
print(model_all.summary())

# ============================================================
# 9. Save all corrected results
# ============================================================
results = {
    'Metric': [
        'Total admissions (MIMIC-IV v3.1)', 
        'Acute abdomen ICD matches',
        'Full dataset N',
        'CC N',
        'CC in-hospital mortality',
        'CC strict ICU mortality',
        'CC ICU survivors who died in hospital',
        'CC mean age',
        'CC age IQR',
        'CC male',
        'CC vasopressor',
        'CC MV',
        'CC surgery',
        'CC lactate median',
        'CC WBC median',
        'CC CCI median',
        'Basic baseline AUC',
        'Extended baseline AUC',
        'Extended+DSI AUC',
        'Extended+all SI AUC',
        'NRI (binary 50%)',
        'IDI',
        'IDI P-value',
        'DSI quartile Q1 hosp mortality',
        'DSI quartile Q2 hosp mortality',
        'DSI quartile Q3 hosp mortality',
        'DSI quartile Q4 hosp mortality',
        'DSI quartile Q1 ICU mortality',
        'DSI quartile Q4 ICU mortality',
        'Bootstrap optimism basic',
        'Bootstrap optimism ext',
        'Bootstrap optimism dsi',
        'Bootstrap optimism all',
    ],
    'Value': [
        546028,
        72676,
        8933,
        5728,
        f"{df_cc[y_col].mean()*100:.1f}% ({df_cc[y_col].sum()})",
        f"{df_cc['icu_death_strict'].mean()*100:.1f}% ({df_cc['icu_death_strict'].sum()})",
        f"{((df_cc['icu_death_strict']==0) & (df_cc[y_col]==1)).sum()} ({((df_cc['icu_death_strict']==0) & (df_cc[y_col]==1)).sum()/df_cc[y_col].sum()*100:.1f}% of hospital deaths)",
        f"{df_cc['age_at_admission'].mean():.1f}",
        f"{df_cc['age_at_admission'].quantile(0.25):.0f}-{df_cc['age_at_admission'].quantile(0.75):.0f}",
        f"{df_cc['gender_male'].mean()*100:.1f}%",
        f"{df_cc['vasopressor_use'].mean()*100:.1f}%",
        f"{df_cc['mechanical_ventilation'].mean()*100:.1f}%",
        f"{df_cc['any_surgery'].mean()*100:.1f}%",
        f"{df_cc['lactate_first'].median():.1f}",
        f"{df_cc['wbc_first'].median():.1f}",
        f"{df_cc['CCI'].median():.0f}",
        f"{auc_basic:.4f}",
        f"{auc_ext:.4f}",
        f"{auc_dsi:.4f}",
        f"{auc_all:.4f}",
        f"{nri_total:.4f}",
        f"{idi:.4f}",
        f"{p_idi:.2e}",
        # Quartile stats
        quartile_stats[0]['Hospital_death_pct'],
        quartile_stats[1]['Hospital_death_pct'],
        quartile_stats[2]['Hospital_death_pct'],
        quartile_stats[3]['Hospital_death_pct'],
        quartile_stats[0]['ICU_death_pct'],
        quartile_stats[3]['ICU_death_pct'],
        f"{optimism_mean_basic:.4f}",
        f"{optimism_mean_ext:.4f}",
        f"{optimism_mean_dsi:.4f}",
        f"{optimism_mean_all:.4f}",
    ]
}

pd.DataFrame(results).to_csv('table_all_results_corrected.csv', index=False)
print("\nSaved: table_all_results_corrected.csv")
print("Saved: table_DSI_quartile_corrected.csv")
print("\n=== DONE ===")
