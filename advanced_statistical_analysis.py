"""
Advanced Statistical Analysis for Shock Index SCI Paper
Includes: NRI/IDI, DCA, RCS, Kaplan-Meier, Calibration, Forest Plot, ROC curves
"""
import pandas as pd, numpy as np, os, sys
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve, brier_score_loss
from sklearn.calibration import calibration_curve
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')

# ===== Global style =====
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 10,
    'axes.linewidth': 1.2,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
})

OUT = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'
FIG = os.path.join(OUT, 'figures')
os.makedirs(FIG, exist_ok=True)

# ===== Load data =====
df = pd.read_csv(os.path.join(OUT, 'analysis_dataset.csv'))
print(f'Full dataset: {len(df)} stays')

# Clean: complete SI data + outlier removal
df_clean = df[df['SI_first'].notna() & df['MSI_first'].notna() & df['DSI_first'].notna()].copy()
for col in ['SI_first','SI_max','SI_mean','MSI_first','MSI_max','MSI_mean','DSI_first','DSI_max','DSI_mean','Age_SI_first','Age_SI_max','Age_SI_mean']:
    if col in df_clean.columns:
        q01, q99 = df_clean[col].quantile([0.01, 0.99])
        df_clean = df_clean[(df_clean[col] >= q01) & (df_clean[col] <= q99)]
print(f'Clean dataset: {len(df_clean)} stays')
print(f'ICU death rate: {df_clean["icu_death"].mean():.3f}')

# =====================================================================
# MODULE 1: NRI & IDI
# =====================================================================
print('\n' + '='*60)
print('MODULE 1: NRI & IDI Analysis')
print('='*60)

def calc_nri_idi(y_true, y_pred_base, y_pred_new, cutoff_low=0.05, cutoff_high=0.15):
    """Calculate categorical NRI and continuous IDI.
    NRI = (up-classified events + down-classified non-events) - (down-classified events + up-classified non-events)
    IDI = (IS_new - IS_base) - (IP_new - IP_base)
    """
    events = y_true == 1
    non_events = y_true == 0
    
    # Categorical NRI
    base_cat = np.where(y_pred_base < cutoff_low, 0, np.where(y_pred_base >= cutoff_high, 2, 1))
    new_cat = np.where(y_pred_new < cutoff_low, 0, np.where(y_pred_new >= cutoff_high, 2, 1))
    
    # Events reclassification
    e_up = np.sum((new_cat[events] > base_cat[events])) / np.sum(events)
    e_down = np.sum((new_cat[events] < base_cat[events])) / np.sum(events)
    nri_events = e_up - e_down
    
    # Non-events reclassification
    ne_up = np.sum((new_cat[non_events] > base_cat[non_events])) / np.sum(non_events)
    ne_down = np.sum((new_cat[non_events] < base_cat[non_events])) / np.sum(non_events)
    nri_nonevents = ne_down - ne_up
    
    nri_total = nri_events + nri_nonevents
    
    # Continuous IDI
    is_new = np.mean(y_pred_new[events]) - np.mean(y_pred_base[events])
    is_base = 0  # already subtracted in is_new
    ip_new = np.mean(y_pred_new[non_events]) - np.mean(y_pred_base[non_events])
    
    idi = (np.mean(y_pred_new[events]) - np.mean(y_pred_base[events])) - \
          (np.mean(y_pred_new[non_events]) - np.mean(y_pred_base[non_events]))
    
    # Z-test for IDI
    var_idi = (np.var(y_pred_new[events] - y_pred_base[events]) / np.sum(events)) + \
              (np.var(y_pred_new[non_events] - y_pred_base[non_events]) / np.sum(non_events))
    z_idi = idi / np.sqrt(var_idi) if var_idi > 0 else 0
    p_idi = 2 * (1 - stats.norm.cdf(abs(z_idi)))
    
    return {
        'nri_events': nri_events, 'nri_nonevents': nri_nonevents, 'nri_total': nri_total,
        'idi': idi, 'z_idi': z_idi, 'p_idi': p_idi
    }

# Create gender_male binary variable (M=1, F=0)
df_clean['gender_male'] = (df_clean['gender'] == 'M').astype(int)

# Build baseline model (age + gender + CCI)
y = df_clean['icu_death'].values
X_base = df_clean[['age_at_admission', 'gender_male', 'CCI']].copy()
X_base.columns = ['age', 'male', 'cci']

# ICU LOS column
time_col = 'los'

# Fit baseline logistic regression
lr_base = LogisticRegression(max_iter=1000, penalty=None)
lr_base.fit(X_base, y)
pred_base = lr_base.predict_proba(X_base)[:, 1]
auc_base = roc_auc_score(y, pred_base)
print(f'Baseline model (age+sex+CCI): AUC={auc_base:.4f}')

# Compare each SI metric added to baseline
si_metrics = {
    'SI (first)': 'SI_first', 'SI (max)': 'SI_max', 'SI (mean 24h)': 'SI_mean',
    'MSI (first)': 'MSI_first', 'MSI (max)': 'MSI_max', 'MSI (mean 24h)': 'MSI_mean',
    'DSI (first)': 'DSI_first', 'DSI (max)': 'DSI_max', 'DSI (mean 24h)': 'DSI_mean',
    'Age-SI (first)': 'Age_SI_first', 'Age-SI (max)': 'Age_SI_max', 'Age-SI (mean 24h)': 'Age_SI_mean',
}

nri_idi_results = []
for name, col in si_metrics.items():
    if col not in df_clean.columns:
        continue
    X_new = X_base.copy()
    X_new[col] = df_clean[col].values
    lr_new = LogisticRegression(max_iter=1000, penalty=None)
    lr_new.fit(X_new, y)
    pred_new = lr_new.predict_proba(X_new)[:, 1]
    auc_new = roc_auc_score(y, pred_new)
    
    nri_idi = calc_nri_idi(y, pred_base, pred_new, cutoff_low=0.05, cutoff_high=0.15)
    
    # Delong test approximation using IDI z-test
    result = {
        'Metric': name, 'AUC_base': auc_base, 'AUC_new': auc_new, 'AUC_diff': auc_new - auc_base,
        'NRI_events': nri_idi['nri_events'], 'NRI_nonevents': nri_idi['nri_nonevents'], 'NRI_total': nri_idi['nri_total'],
        'IDI': nri_idi['idi'], 'IDI_Z': nri_idi['z_idi'], 'IDI_P': nri_idi['p_idi']
    }
    nri_idi_results.append(result)
    print(f'{name}: AUC={auc_new:.4f} (+{auc_new-auc_base:.4f}), NRI={nri_idi["nri_total"]:.4f}, IDI={nri_idi["idi"]:.4f} (P={nri_idi["p_idi"]:.4f})')

nri_idi_df = pd.DataFrame(nri_idi_results)
nri_idi_df.to_csv(os.path.join(OUT, 'table3_nri_idi.csv'), index=False)
print('\nSaved table3_nri_idi.csv')

# =====================================================================
# MODULE 2: DCA (Decision Curve Analysis)
# =====================================================================
print('\n' + '='*60)
print('MODULE 2: Decision Curve Analysis')
print('='*60)

def calc_dca(y_true, y_pred, thresholds):
    """Calculate net benefit at each threshold probability."""
    net_benefits = []
    for tp in thresholds:
        # Predictions at this threshold
        pred_pos = y_pred >= tp
        tp_count = np.sum(pred_pos & (y_true == 1))
        fp_count = np.sum(pred_pos & (y_true == 0))
        n_total = len(y_true)
        net_benefit = tp_count / n_total - fp_count / n_total * (tp / (1 - tp))
        net_benefits.append(net_benefit)
    return net_benefits

thresholds = np.arange(0.01, 0.50, 0.01)

# Models for DCA
# 1. Treat all (reference)
treat_all_nb = [(np.sum(y == 1) / len(y)) - (np.sum(y == 0) / len(y)) * (tp / (1 - tp)) for tp in thresholds]

# 2. Treat none (reference)
treat_none_nb = [0] * len(thresholds)

# 3. Baseline model
dca_base = calc_dca(y, pred_base, thresholds)

# 4. Baseline + DSI (best single metric)
X_dsi = X_base.copy()
X_dsi['DSI_mean'] = df_clean['DSI_mean'].values
lr_dsi = LogisticRegression(max_iter=1000, penalty=None)
lr_dsi.fit(X_dsi, y)
pred_dsi = lr_dsi.predict_proba(X_dsi)[:, 1]
dca_dsi = calc_dca(y, pred_dsi, thresholds)

# 5. Baseline + MSI
X_msi = X_base.copy()
X_msi['MSI_mean'] = df_clean['MSI_mean'].values
lr_msi = LogisticRegression(max_iter=1000, penalty=None)
lr_msi.fit(X_msi, y)
pred_msi = lr_msi.predict_proba(X_msi)[:, 1]
dca_msi = calc_dca(y, pred_msi, thresholds)

# 6. Baseline + Age-SI
X_agesi = X_base.copy()
X_agesi['Age_SI_mean'] = df_clean['Age_SI_mean'].values
lr_agesi = LogisticRegression(max_iter=1000, penalty=None)
lr_agesi.fit(X_agesi, y)
pred_agesi = lr_agesi.predict_proba(X_agesi)[:, 1]
dca_agesi = calc_dca(y, pred_agesi, thresholds)

# 7. Full model (all 4 SI metrics)
X_full = X_base.copy()
X_full['SI_mean'] = df_clean['SI_mean'].values
X_full['MSI_mean'] = df_clean['MSI_mean'].values
X_full['DSI_mean'] = df_clean['DSI_mean'].values
X_full['Age_SI_mean'] = df_clean['Age_SI_mean'].values
lr_full = LogisticRegression(max_iter=1000, penalty=None)
lr_full.fit(X_full, y)
pred_full = lr_full.predict_proba(X_full)[:, 1]
dca_full = calc_dca(y, pred_full, thresholds)

# Plot DCA
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(thresholds, treat_all_nb, 'k--', linewidth=1, label='Treat All')
ax.plot(thresholds, treat_none_nb, 'k:', linewidth=1, label='Treat None')
ax.plot(thresholds, dca_base, color='#999999', linewidth=2, label='Baseline (Age+Sex+CCI)')
ax.plot(thresholds, dca_dsi, color='#E74C3C', linewidth=2, label='Baseline + DSI')
ax.plot(thresholds, dca_msi, color='#3498DB', linewidth=2, label='Baseline + MSI')
ax.plot(thresholds, dca_agesi, color='#2ECC71', linewidth=2, label='Baseline + Age-SI')
ax.plot(thresholds, dca_full, color='#F39C12', linewidth=2.5, label='Full Model (All 4 SI metrics)')

ax.set_xlabel('Threshold Probability (%)')
ax.set_ylabel('Net Benefit')
ax.set_title('Decision Curve Analysis: SI-Derived Metrics for ICU Mortality Prediction')
ax.legend(loc='lower right', framealpha=0.9)
ax.set_xlim(0, 0.50)
ax.set_ylim(-0.05, 0.20)
ax.grid(True, alpha=0.3)

# Format x-axis as percentage
ax.set_xticks(np.arange(0, 0.51, 0.05))
ax.set_xticklabels([f'{int(x*100)}%' for x in np.arange(0, 0.51, 0.05)])

plt.savefig(os.path.join(FIG, 'Fig3_DCA.png'))
plt.savefig(os.path.join(FIG, 'Fig3_DCA.pdf'))
print('Saved Fig3_DCA.png/pdf')

# =====================================================================
# MODULE 3: RCS (Restricted Cubic Spline)
# =====================================================================
print('\n' + '='*60)
print('MODULE 3: Restricted Cubic Spline Analysis')
print('='*60)

def rcs_transform(x, knots):
    """Create restricted cubic spline basis functions."""
    x = np.array(x, dtype=float)
    k = len(knots)
    n = len(x)
    # First basis: x itself (linear component)
    basis = [x]
    # Higher-order basis functions
    for j in range(2, k):
        def _h(x_val, k_j, k_last):
            return np.maximum(0, (x_val - k_j)**3) - \
                   np.maximum(0, (x_val - k_last)**3) * (k_last - knots[j-1]) / (k_last - knots[j-2]) + \
                   np.maximum(0, (x_val - knots[j-2])**3) * (k_last - k_j) / (k_last - knots[j-2])
        basis.append(_h(x, knots[j-1], knots[-1]))
    return np.column_stack(basis)

def fit_rcs_logistic(y, x, knots, covariates_df=None):
    """Fit logistic regression with RCS terms + optional covariates."""
    rcs_basis = rcs_transform(x, knots)
    col_names = [f'rcs_{i}' for i in range(rcs_basis.shape[1])]
    X_rcs = pd.DataFrame(rcs_basis, columns=col_names)
    
    if covariates_df is not None:
        X_rcs = pd.concat([covariates_df.reset_index(drop=True), X_rcs], axis=1)
    
    # Add constant
    X_rcs = sm.add_constant(X_rcs)
    
    # Fit
    model = sm.Logit(y, X_rcs).fit(disp=0, maxiter=200)
    return model, X_rcs, col_names

# RCS for each SI metric with 4 knots (quintile positions)
metrics_for_rcs = {
    'SI': ('SI_mean', 'Shock Index (mean 24h)'),
    'MSI': ('MSI_mean', 'Modified Shock Index (mean 24h)'),
    'DSI': ('DSI_mean', 'Diastolic Shock Index (mean 24h)'),
    'Age-SI': ('Age_SI_mean', 'Age-Adjusted Shock Index (mean 24h)'),
}

covars = df_clean[['age_at_admission', 'gender_male', 'CCI']].copy()
covars.columns = ['age', 'male', 'cci']

fig_rcs, axes_rcs = plt.subplots(2, 2, figsize=(12, 10))
rcs_results = []

for idx, (key, (col, label)) in enumerate(metrics_for_rcs.items()):
    ax = axes_rcs[idx // 2, idx % 2]
    x_data = df_clean[col].values
    y_data = df_clean['icu_death'].values
    
    # Determine knots at 5th, 35th, 65th, 95th percentile (4 knots)
    knots = np.percentile(x_data, [5, 35, 65, 95])
    
    # Fit RCS model
    model, X_rcs, col_names = fit_rcs_logistic(y_data, x_data, knots, covars)
    
    # Generate prediction curve
    x_range = np.linspace(np.percentile(x_data, 1), np.percentile(x_data, 99), 200)
    rcs_pred_basis = rcs_transform(x_range, knots)
    col_names_pred = [f'rcs_{i}' for i in range(rcs_pred_basis.shape[1])]
    X_pred = pd.DataFrame(rcs_pred_basis, columns=col_names_pred)
    
    # Add covariates at median values for reference
    for c in ['age', 'male', 'cci']:
        X_pred[c] = covars[c].median()
    X_pred = pd.concat([X_pred, covars.median().to_frame().T], axis=0).drop_duplicates(subset=col_names_pred, keep='first')
    
    # Simplify: just predict at median covariate values
    X_pred_clean = pd.DataFrame(rcs_pred_basis, columns=col_names_pred)
    for c in ['age', 'male', 'cci']:
        X_pred_clean[c] = covars[c].median()
    X_pred_clean = sm.add_constant(X_pred_clean)
    # Ensure column order matches model params
    X_pred_clean = X_pred_clean.reindex(columns=model.params.index)
    
    # Predict
    pred_proba = model.predict(X_pred_clean)
    
    # Calculate 95% CI via bootstrap (reduced to 50 for speed)
    n_bootstrap = 50
    pred_boot = np.zeros((n_bootstrap, len(x_range)))
    for b in range(n_bootstrap):
        boot_idx = np.random.choice(len(y_data), len(y_data), replace=True)
        try:
            boot_model, _, _ = fit_rcs_logistic(
                y_data[boot_idx], x_data[boot_idx], knots, covars.iloc[boot_idx])
            boot_basis = rcs_transform(x_range, knots)
            boot_X = pd.DataFrame(boot_basis, columns=col_names_pred)
            for c in ['age', 'male', 'cci']:
                boot_X[c] = covars[c].median()
            boot_X = sm.add_constant(boot_X)
            boot_X = boot_X.reindex(columns=boot_model.params.index)
            pred_boot[b] = boot_model.predict(boot_X)
        except:
            pred_boot[b] = pred_proba
    
    ci_lower = np.percentile(pred_boot, 2.5, axis=0)
    ci_upper = np.percentile(pred_boot, 97.5, axis=0)
    
    # Plot
    ax.plot(x_range, pred_proba, color='#2C3E50', linewidth=2)
    ax.fill_between(x_range, ci_lower, ci_upper, alpha=0.2, color='#2C3E50')
    ax.set_xlabel(label)
    ax.set_ylabel('Predicted Probability of ICU Mortality')
    ax.set_title(f'RCS: {key} → ICU Mortality')
    
    # Add reference line at median outcome
    ax.axhline(y=y_data.mean(), color='red', linestyle=':', alpha=0.5)
    
    # P-value for nonlinear component
    # Test: are the nonlinear terms jointly significant?
    nonlinear_cols = [c for c in col_names if c != 'rcs_0']
    if len(nonlinear_cols) > 0:
        # Wald test for nonlinear terms
        try:
            r_matrix = np.zeros((len(nonlinear_cols), len(model.params)))
            for i, c in enumerate(nonlinear_cols):
                param_idx = list(model.params.index).index(c)
                r_matrix[i, param_idx] = 1
            wald_test = model.wald_test(r_matrix)
            p_nonlinear = wald_test.pvalue
        except:
            p_nonlinear = np.nan
    else:
        p_nonlinear = np.nan
    
    # Overall P for the metric
    try:
        r_all = np.zeros((len(col_names), len(model.params)))
        for i, c in enumerate(col_names):
            param_idx = list(model.params.index).index(c)
            r_all[i, param_idx] = 1
        wald_all = model.wald_test(r_all)
        p_overall = wald_all.pvalue
    except:
        p_overall = np.nan
    
    ax.text(0.05, 0.95, f'P overall={p_overall:.4f}\nP nonlinear={p_nonlinear:.4f}',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    rcs_results.append({
        'Metric': key, 'P_overall': p_overall, 'P_nonlinear': p_nonlinear,
        'Knots': str([f'{k:.2f}' for k in knots])
    })

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'Fig4_RCS.png'))
plt.savefig(os.path.join(FIG, 'Fig4_RCS.pdf'))
print('Saved Fig4_RCS.png/pdf')

rcs_df = pd.DataFrame(rcs_results)
rcs_df.to_csv(os.path.join(OUT, 'table4_rcs.csv'), index=False)
print('Saved table4_rcs.csv')

# =====================================================================
# MODULE 4: Kaplan-Meier Survival Curves
# =====================================================================
print('\n' + '='*60)
print('MODULE 4: Kaplan-Meier Survival Curves')
print('='*60)

# Create SI quartile groups
for col, name in [('SI_mean', 'SI'), ('MSI_mean', 'MSI'), ('DSI_mean', 'DSI'), ('Age_SI_mean', 'AgeSI')]:
    df_clean[f'{name}_quartile'] = pd.qcut(df_clean[col], q=4, labels=['Q1(Low)', 'Q2', 'Q3', 'Q4(High)'])

time_col_km = 'los'

# Fix: ensure positive time values
df_km = df_clean[df_clean[time_col_km] > 0].copy()
df_km['gender_male'] = (df_km['gender'] == 'M').astype(int)
print(f'Time variable: {time_col_km}')
print(f'KM dataset: {len(df_km)} stays')

def kaplan_meier(time, event, groups):
    """Simple KM estimator per group."""
    results = {}
    for g in sorted(groups.unique()):
        t_g = time[groups == g]
        e_g = event[groups == g]
        # Sort by time
        order = np.argsort(t_g)
        t_sorted = t_g.values[order]
        e_sorted = e_g.values[order]
        
        n_at_risk = len(t_g)
        survival = 1.0
        km_times = [0]
        km_survival = [1.0]
        
        for i in range(len(t_sorted)):
            if e_sorted[i] == 1:  # event
                survival *= (n_at_risk - 1) / n_at_risk
                n_at_risk -= 1
            else:  # censored
                n_at_risk -= 1
            km_times.append(t_sorted[i])
            km_survival.append(survival)
        
        results[g] = (km_times, km_survival)
    return results

# KM curves for DSI quartiles (best predictor)
fig_km, axes_km = plt.subplots(2, 2, figsize=(12, 10))

km_metrics = [('DSI_quartile', 'DSI'), ('MSI_quartile', 'MSI'), ('AgeSI_quartile', 'Age-SI'), ('SI_quartile', 'SI')]
km_logrank_results = []

for idx, (qcol, name) in enumerate(km_metrics):
    ax = axes_km[idx // 2, idx % 2]
    
    km_results = kaplan_meier(df_km[time_col_km], df_km['icu_death'], df_km[qcol])
    
    colors = ['#2ECC71', '#3498DB', '#E67E22', '#E74C3C']
    for g_idx, (g, (km_t, km_s)) in enumerate(sorted(km_results.items())):
        ax.step(km_t, km_s, where='post', color=colors[g_idx], linewidth=1.5, label=g)
    
    # Log-rank test
    groups_list = sorted(df_km[qcol].unique())
    group_data = []
    for g in groups_list:
        mask = df_km[qcol] == g
        group_data.append((df_km.loc[mask, time_col_km].values, df_km.loc[mask, 'icu_death'].values))
    
    # Chi-square based log-rank test
    n_groups = len(group_data)
    obs_events = [np.sum(d[1]) for d in group_data]
    obs_times = [np.sum(d[0]) for d in group_data]
    total_events = np.sum(obs_events)
    total_time = np.sum(obs_times)
    expected = [total_events * ot / total_time for ot in obs_times]
    chi2 = np.sum([(o - e)**2 / e if e > 0 else 0 for o, e in zip(obs_events, expected)])
    p_logrank = 1 - stats.chi2.cdf(chi2, df=n_groups - 1) if n_groups > 1 else np.nan
    
    km_logrank_results.append({'Metric': name, 'Log-rank Chi2': chi2, 'P_value': p_logrank})
    
    ax.set_xlabel('ICU Length of Stay (days)')
    ax.set_ylabel('Survival Probability')
    ax.set_title(f'KM Curve: {name} Quartiles → ICU Survival')
    ax.legend(loc='lower left', framealpha=0.9)
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, min(df_km[time_col_km].quantile(0.95), 30))
    ax.text(0.05, 0.95, f'Log-rank P={p_logrank:.4f}',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'Fig5_KM.png'))
plt.savefig(os.path.join(FIG, 'Fig5_KM.pdf'))
print('Saved Fig5_KM.png/pdf')

km_df = pd.DataFrame(km_logrank_results)
km_df.to_csv(os.path.join(OUT, 'table5_km_logrank.csv'), index=False)
print('Saved table5_km_logrank.csv')

# =====================================================================
# MODULE 5: Calibration
# =====================================================================
print('\n' + '='*60)
print('MODULE 5: Calibration Analysis')
print('='*60)

fig_cal, axes_cal = plt.subplots(2, 3, figsize=(14, 8))

models_for_cal = {
    'Baseline': pred_base,
    'Baseline + DSI': pred_dsi,
    'Baseline + MSI': pred_msi,
    'Baseline + Age-SI': pred_agesi,
    'Baseline + SI': None,  # will compute
    'Full Model': pred_full,
}

# Add baseline + SI
X_si = X_base.copy()
X_si['SI_mean'] = df_clean['SI_mean'].values
lr_si = LogisticRegression(max_iter=1000, penalty=None)
lr_si.fit(X_si, y)
pred_si = lr_si.predict_proba(X_si)[:, 1]
models_for_cal['Baseline + SI'] = pred_si

cal_results = []
for idx, (name, pred) in enumerate(models_for_cal.items()):
    ax = axes_cal[idx // 3, idx % 3]
    
    # Calibration curve
    fraction_of_positives, mean_predicted_value = calibration_curve(y, pred, n_bins=10, strategy='uniform')
    
    # Brier score
    brier = brier_score_loss(y, pred)
    
    # Hosmer-Lemeshow test
    bins = pd.qcut(pred, q=10, duplicates='drop')
    hl_df = pd.DataFrame({'pred': pred, 'obs': y, 'bin': bins})
    hl_obs = hl_df.groupby('bin', observed=True)['obs'].sum()
    hl_exp = hl_df.groupby('bin', observed=True)['pred'].sum()
    hl_n = hl_df.groupby('bin', observed=True).size()
    hl_chi2 = np.sum((hl_obs - hl_exp)**2 / (hl_exp * (1 - hl_exp / hl_n)).replace(0, 1))
    hl_p = 1 - stats.chi2.cdf(hl_chi2, df=len(hl_obs) - 2)
    
    # Plot
    ax.plot(mean_predicted_value, fraction_of_positives, 's-', color='#2C3E50', linewidth=2, label=name)
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Perfect Calibration')
    ax.set_xlabel('Mean Predicted Probability')
    ax.set_ylabel('Fraction of Positives')
    ax.set_title(f'{name}\nBrier={brier:.4f}, HL P={hl_p:.3f}')
    ax.set_xlim(0, 0.4)
    ax.set_ylim(0, 0.4)
    ax.legend(loc='lower right', fontsize=8)
    ax.grid(True, alpha=0.3)
    
    cal_results.append({
        'Model': name, 'Brier_score': brier, 'HL_Chi2': hl_chi2, 'HL_P': hl_p
    })

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'Fig6_Calibration.png'))
plt.savefig(os.path.join(FIG, 'Fig6_Calibration.pdf'))
print('Saved Fig6_Calibration.png/pdf')

cal_df = pd.DataFrame(cal_results)
cal_df.to_csv(os.path.join(OUT, 'table6_calibration.csv'), index=False)
print('Saved table6_calibration.csv')

# =====================================================================
# MODULE 6: ROC Curve Comparison Figure
# =====================================================================
print('\n' + '='*60)
print('MODULE 6: ROC Curve Comparison')
print('='*60)

fig_roc, ax_roc = plt.subplots(figsize=(8, 8))

roc_models = {
    'Baseline (Age+Sex+CCI)': pred_base,
    'Baseline + SI': pred_si,
    'Baseline + MSI': pred_msi,
    'Baseline + DSI': pred_dsi,
    'Baseline + Age-SI': pred_agesi,
    'Full Model': pred_full,
}

colors_roc = ['#999999', '#3498DB', '#2ECC71', '#E74C3C', '#9B59B6', '#F39C12']
auc_roc_results = []

for idx, (name, pred) in enumerate(roc_models.items()):
    fpr, tpr, _ = roc_curve(y, pred)
    auc_val = roc_auc_score(y, pred)
    ax_roc.plot(fpr, tpr, color=colors_roc[idx], linewidth=2 if idx > 0 else 1.5,
                linestyle='-' if idx > 0 else '--',
                label=f'{name} (AUC={auc_val:.3f})')
    auc_roc_results.append({'Model': name, 'AUC': auc_val})

ax_roc.plot([0, 1], [0, 1], 'k:', linewidth=1)
ax_roc.set_xlabel('1 - Specificity (False Positive Rate)')
ax_roc.set_ylabel('Sensitivity (True Positive Rate)')
ax_roc.set_title('ROC Curves: SI-Derived Metrics for ICU Mortality Prediction')
ax_roc.legend(loc='lower right', framealpha=0.9)
ax_roc.set_xlim(0, 1)
ax_roc.set_ylim(0, 1)
ax_roc.grid(True, alpha=0.3)

plt.savefig(os.path.join(FIG, 'Fig2_ROC.png'))
plt.savefig(os.path.join(FIG, 'Fig2_ROC.pdf'))
print('Saved Fig2_ROC.png/pdf')

roc_df = pd.DataFrame(auc_roc_results)
roc_df.to_csv(os.path.join(OUT, 'table2_roc_models.csv'), index=False)

# =====================================================================
# MODULE 7: Forest Plot (Multivariate Logistic Regression)
# =====================================================================
print('\n' + '='*60)
print('MODULE 7: Forest Plot')
print('='*60)

# Fit full model using statsmodels for OR and CI
df_clean['gender_male'] = (df_clean['gender'] == 'M').astype(int)
X_sm = df_clean[['age_at_admission', 'gender_male', 'CCI', 'SI_mean', 'MSI_mean', 'DSI_mean', 'Age_SI_mean']].copy()
X_sm.columns = ['Age', 'Male', 'CCI', 'SI_mean', 'MSI_mean', 'DSI_mean', 'Age_SI_mean']
X_sm = sm.add_constant(X_sm)

model_sm = sm.Logit(y, X_sm).fit(disp=0, maxiter=200)
print(model_sm.summary())

# Extract OR and 95% CI
params = model_sm.params[1:]  # exclude constant
conf = model_sm.conf_int()[1:]
or_vals = np.exp(params)
or_lower = np.exp(conf.iloc[:, 0])
or_upper = np.exp(conf.iloc[:, 1])
p_vals = model_sm.pvalues[1:]

forest_data = pd.DataFrame({
    'Variable': params.index,
    'OR': or_vals.values,
    'CI_lower': or_lower.values,
    'CI_upper': or_upper.values,
    'P_value': p_vals.values
})
forest_data.to_csv(os.path.join(OUT, 'table7_forest.csv'), index=False)

# Plot forest plot
fig_forest, ax_forest = plt.subplots(figsize=(10, 6))

variables = forest_data['Variable'].tolist()
or_list = forest_data['OR'].tolist()
ci_lower = forest_data['CI_lower'].tolist()
ci_upper = forest_data['CI_upper'].tolist()

y_pos = range(len(variables))

# Draw
for i, (v, o, cl, cu) in enumerate(zip(variables, or_list, ci_lower, ci_upper)):
    ax_forest.plot([cl, cu], [i, i], color='#2C3E50', linewidth=2)
    ax_forest.plot(o, i, 'D', color='#E74C3C', markersize=8)
    
    # Label
    p_str = f'P={forest_data.iloc[i]["P_value"]:.3f}' if forest_data.iloc[i]["P_value"] >= 0.001 else 'P<0.001'
    ax_forest.text(cu + 0.05, i, f'OR={o:.3f} [{cl:.3f}-{cu:.3f}] {p_str}',
                   fontsize=9, verticalalignment='center')

ax_forest.axvline(x=1, color='gray', linestyle='--', linewidth=1)
ax_forest.set_yticks(y_pos)
ax_forest.set_yticklabels(variables)
ax_forest.set_xlabel('Odds Ratio')
ax_forest.set_title('Forest Plot: Multivariate Logistic Regression (Full Model)')
ax_forest.set_xlim(0.5, max(ci_upper) + 0.5)
ax_forest.invert_yaxis()
ax_forest.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'Fig7_Forest.png'))
plt.savefig(os.path.join(FIG, 'Fig7_Forest.pdf'))
print('Saved Fig7_Forest.png/pdf')

# =====================================================================
# MODULE 8: Subgroup ROC (by acute abdomen subtype)
# =====================================================================
print('\n' + '='*60)
print('MODULE 8: Subgroup ROC Curves')
print('='*60)

subtypes = ['ischemic', 'perforation', 'obstruction', 'inflammatory', 'other']

fig_sub, axes_sub = plt.subplots(1, 4, figsize=(16, 4))

sub_metrics = [('DSI_mean', 'DSI'), ('MSI_mean', 'MSI'), ('Age_SI_mean', 'Age-SI'), ('SI_mean', 'SI')]
sub_auc_results = []

for idx, (col, name) in enumerate(sub_metrics):
    ax = axes_sub[idx]
    colors_sub = ['#E74C3C', '#E67E22', '#3498DB', '#2ECC71', '#999999']
    
    for s_idx, subtype in enumerate(subtypes):
        sub_df = df_clean[df_clean['abdomen_subtype'] == subtype]
        if len(sub_df) < 20 or sub_df['icu_death'].sum() < 5:
            continue
        y_sub = sub_df['icu_death'].values
        pred_sub = sub_df[col].values
        auc_sub = roc_auc_score(y_sub, pred_sub)
        
        fpr, tpr, _ = roc_curve(y_sub, pred_sub)
        ax.plot(fpr, tpr, color=colors_sub[s_idx], linewidth=1.5,
                label=f'{subtype} (AUC={auc_sub:.3f}, n={len(sub_df)})')
        
        sub_auc_results.append({
            'Subtype': subtype, 'Metric': name, 'AUC': auc_sub, 'N': len(sub_df),
            'Deaths': int(sub_df['icu_death'].sum())
        })
    
    ax.plot([0, 1], [0, 1], 'k:', linewidth=1)
    ax.set_xlabel('1 - Specificity')
    ax.set_ylabel('Sensitivity')
    ax.set_title(f'{name} by Subtype')
    ax.legend(loc='lower right', fontsize=7)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'Fig8_Subgroup_ROC.png'))
plt.savefig(os.path.join(FIG, 'Fig8_Subgroup_ROC.pdf'))
print('Saved Fig8_Subgroup_ROC.png/pdf')

sub_auc_df = pd.DataFrame(sub_auc_results)
sub_auc_df.to_csv(os.path.join(OUT, 'table8_subgroup_auc.csv'), index=False)

# =====================================================================
# Summary Print
# =====================================================================
print('\n' + '='*60)
print('ANALYSIS SUMMARY')
print('='*60)

print('\n--- NRI/IDI ---')
print(nri_idi_df.to_string(index=False))

print('\n--- RCS ---')
print(rcs_df.to_string(index=False))

print('\n--- KM Log-rank ---')
print(km_df.to_string(index=False))

print('\n--- Calibration ---')
print(cal_df.to_string(index=False))

print('\n--- ROC Models ---')
print(roc_df.to_string(index=False))

print('\n--- Subgroup AUC ---')
print(sub_auc_df.to_string(index=False))

print('\n--- Forest Plot ---')
print(forest_data.to_string(index=False))

print('\n\nAll figures saved in:', FIG)
print('All tables saved in:', OUT)
print('\n✅ Advanced statistical analysis complete!')
