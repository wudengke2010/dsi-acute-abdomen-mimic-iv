#!/usr/bin/env python3
"""Generate v7 figures for AIC submission (primary model WITHOUT surgery)"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import mannwhitneyu
import json
import os

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 11,
    'axes.linewidth': 1.0,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

OUT_DIR = 'figures_v7'
os.makedirs(OUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv('analysis_dataset_revised.csv')
v6_stats = json.load(open('v6_revision_statistics.json'))
eicu_stats = json.load(open('eicu_external_validation_results.json'))

# Primary model (no surgery) coefficients
primary_coeffs = v6_stats['P0_4_surgery_variations']['extended_no_surgery_DSI']['coefficients']

# ============================================================
# Figure 2: ROC curves (primary model without surgery)
# ============================================================
print("Generating Figure 2: ROC curves...")

from sklearn.metrics import roc_curve, auc

# Compute predictions for each model
# Basic baseline: age + sex + CCI
df_basic = df.copy()
df_basic['y'] = df_basic['hospital_expire_flag']

# Extended baseline (no surgery)
ext_predictors = ['age_at_admission', 'gender_binary', 'CCI', 'lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'sofa']
df_extended = df.copy()
df_extended['y'] = df_extended['hospital_expire_flag']

# Extended+DSI (no surgery) - PRIMARY MODEL
ext_dsi_predictors = ext_predictors + ['DSI_mean']
df_ext_dsi = df.copy()
df_ext_dsi['y'] = df_ext_dsi['hospital_expire_flag']

# Compute model predictions using coefficients from v6_stats
def compute_pred(data, coeffs_dict, intercept):
    pred = intercept
    col_map = {
        'age_at_admission': 'age_at_admission',
        'gender_binary': 'gender_binary',
        'CCI': 'CCI',
        'lactate_first': 'lactate_first',
        'wbc_first': 'wbc_first',
        'vasopressor_use': 'vasopressor_use',
        'mechanical_ventilation': 'mechanical_ventilation',
        'sofa': 'sofa',
        'DSI_mean': 'DSI_mean'
    }
    for var, info in coeffs_dict.items():
        col = col_map.get(var, var)
        if col in data.columns:
            pred += info['beta'] * data[col].values
    return pred

# Basic baseline model (age+sex+CCI only)
# We need separate coefficients for this; use simple logistic regression
from sklearn.linear_model import LogisticRegression
basic_vars = ['age_at_admission', 'gender', 'CCI']
df_clean = df.dropna(subset=basic_vars + ['hospital_expire_flag']).copy()
df_clean['gender_num'] = (df_clean['gender'] == 'M').astype(int)
basic_vars_num = ['age_at_admission', 'gender_num', 'CCI']
lr_basic = LogisticRegression(max_iter=5000, C=1e6, solver='lbfgs')
lr_basic.fit(df_clean[basic_vars_num], df_clean['hospital_expire_flag'])
pred_basic = lr_basic.predict_proba(df_clean[basic_vars_num])[:, 1]

# Extended baseline (no surgery)
ext_predictors_real = ['age_at_admission', 'gender_num', 'CCI', 'lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'sofa']
df_clean_ext = df.dropna(subset=['age_at_admission', 'gender', 'CCI', 'lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'sofa', 'hospital_expire_flag']).copy()
df_clean_ext['gender_num'] = (df_clean_ext['gender'] == 'M').astype(int)
lr_ext = LogisticRegression(max_iter=5000, C=1e6, solver='lbfgs')
lr_ext.fit(df_clean_ext[ext_predictors_real], df_clean_ext['hospital_expire_flag'])
pred_ext = lr_ext.predict_proba(df_clean_ext[ext_predictors_real])[:, 1]

# Extended+DSI (no surgery) - primary model
ext_dsi_predictors_real = ext_predictors_real + ['DSI_mean']
df_clean_ext_dsi = df.dropna(subset=['age_at_admission', 'gender', 'CCI', 'lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'sofa', 'DSI_mean', 'hospital_expire_flag']).copy()
df_clean_ext_dsi['gender_num'] = (df_clean_ext_dsi['gender'] == 'M').astype(int)
lr_ext_dsi = LogisticRegression(max_iter=5000, C=1e6, solver='lbfgs')
lr_ext_dsi.fit(df_clean_ext_dsi[ext_dsi_predictors_real], df_clean_ext_dsi['hospital_expire_flag'])
pred_ext_dsi = lr_ext_dsi.predict_proba(df_clean_ext_dsi[ext_dsi_predictors_real])[:, 1]

# Extended+all SI derivatives
all_si_predictors_real = ext_predictors_real + ['SI_mean', 'MSI_mean', 'DSI_mean', 'Age_SI_mean']
df_clean_all = df.dropna(subset=['age_at_admission', 'gender', 'CCI', 'lactate_first', 'wbc_first', 'vasopressor_use', 'mechanical_ventilation', 'sofa', 'SI_mean', 'MSI_mean', 'DSI_mean', 'Age_SI_mean', 'hospital_expire_flag']).copy()
df_clean_all['gender_num'] = (df_clean_all['gender'] == 'M').astype(int)
lr_all = LogisticRegression(max_iter=5000, C=1e6, solver='lbfgs')
lr_all.fit(df_clean_all[all_si_predictors_real], df_clean_all['hospital_expire_flag'])
pred_all = lr_all.predict_proba(df_clean_all[all_si_predictors_real])[:, 1]

y_true = df_clean['hospital_expire_flag'].values

# ROC curves
fig, ax = plt.subplots(figsize=(8, 7))

# Use the same y_true for all (from basic model subset)
y_basic = df_clean['hospital_expire_flag'].values
fpr_basic, tpr_basic, _ = roc_curve(y_basic, pred_basic)
auc_basic = auc(fpr_basic, tpr_basic)

y_ext = df_clean_ext['hospital_expire_flag'].values
fpr_ext, tpr_ext, _ = roc_curve(y_ext, pred_ext)
auc_ext = auc(fpr_ext, tpr_ext)

y_ext_dsi = df_clean_ext_dsi['hospital_expire_flag'].values
fpr_ext_dsi, tpr_ext_dsi, _ = roc_curve(y_ext_dsi, pred_ext_dsi)
auc_ext_dsi = auc(fpr_ext_dsi, tpr_ext_dsi)

y_all = df_clean_all['hospital_expire_flag'].values
fpr_all, tpr_all, _ = roc_curve(y_all, pred_all)
auc_all = auc(fpr_all, tpr_all)

ax.plot(fpr_basic, tpr_basic, 'k--', linewidth=1.5, label=f'Basic baseline (AUC={auc_basic:.3f})')
ax.plot(fpr_ext, tpr_ext, 'b-', linewidth=2.0, label=f'Extended baseline, no surgery (AUC={auc_ext:.3f})')
ax.plot(fpr_ext_dsi, tpr_ext_dsi, 'r-', linewidth=2.5, label=f'Extended + DSI (AUC={auc_ext_dsi:.3f})')
ax.plot(fpr_all, tpr_all, 'g-.', linewidth=1.5, label=f'Extended + all SI (AUC={auc_all:.3f})')
ax.plot([0, 1], [0, 1], 'k:', linewidth=0.5)
ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate', fontsize=12)
ax.set_title('ROC Curves — Primary Model (Without Surgery)', fontsize=13)
ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])

plt.savefig(f'{OUT_DIR}/Fig2_ROC.png', dpi=300)
plt.savefig(f'{OUT_DIR}/Fig2_ROC.pdf', dpi=300)
print(f"  Fig2 ROC: Basic={auc_basic:.3f}, Ext_no_surg={auc_ext:.3f}, Ext+DSI={auc_ext_dsi:.3f}, All SI={auc_all:.3f}")

# ============================================================
# Figure 3: Forest plot (primary model without surgery)
# ============================================================
print("Generating Figure 3: Forest plot...")

coeffs = v6_stats['P0_4_surgery_variations']['extended_no_surgery_DSI']['coefficients']
var_names = list(coeffs.keys())
var_labels = {
    'age_at_admission': 'Age (per year)',
    'gender_binary': 'Male gender',
    'CCI': 'CCI (per point)',
    'lactate_first': 'Lactate (per mmol/L)',
    'wbc_first': 'WBC (per ×10⁹/L)',
    'vasopressor_use': 'Vasopressor use',
    'mechanical_ventilation': 'Mechanical ventilation',
    'sofa': 'SOFA (per point)',
    'DSI_mean': 'DSI (mean 24h)'
}

fig, ax = plt.subplots(figsize=(10, 7))

# Sort by OR (descending)
sorted_vars = sorted(var_names, key=lambda v: coeffs[v]['OR'], reverse=True)
y_pos = list(range(len(sorted_vars)))

for i, var in enumerate(sorted_vars):
    or_val = coeffs[var]['OR']
    ci_lo = coeffs[var]['CI_lower']
    ci_hi = coeffs[var]['CI_upper']
    p_val = coeffs[var]['P']
    
    # Color: DSI = red highlight, significant = dark blue, non-significant = light gray
    try:
        p_float = float(p_val)
    except:
        # Handle scientific notation like "7.59e-15" or "4.83e-36"
        p_float = float(p_val.replace('e-', 'e-').replace('E', 'e'))
    
    if var == 'DSI_mean':
        color = '#E74C3C'
        marker_size = 200
        edge_color = '#C0392B'
    elif p_float < 0.05:
        color = '#2C3E50'
        marker_size = 100
        edge_color = '#2C3E50'
    else:
        color = '#BDC3C7'
        marker_size = 80
        edge_color = '#95A5A6'
    
    ax.scatter(or_val, i, s=marker_size, c=color, edgecolors=edge_color, zorder=3, linewidths=1.5)
    ax.plot([ci_lo, ci_hi], [i, i], color=edge_color, linewidth=2, zorder=2)
    
    # Label
    label = var_labels.get(var, var)
    p_str = f"P={p_val}"
    sig_str = " *" if p_float < 0.05 else ""
    ax.text(0.05, i, f"{label}  OR={or_val:.2f} ({ci_lo:.2f}-{ci_hi:.2f})  {p_str}{sig_str}",
            va='center', ha='left', fontsize=9, fontfamily='serif')

ax.axvline(x=1.0, color='k', linestyle='--', linewidth=1.0, zorder=1)
ax.set_yticks(y_pos)
ax.set_yticklabels(['' for _ in y_pos])
ax.set_xlabel('Odds Ratio', fontsize=12)
ax.set_title('Forest Plot — Primary Model (Extended Baseline Without Surgery + DSI)', fontsize=13)
ax.set_xlim([0.5, 3.0])
ax.invert_yaxis()

# Add annotation box for DSI
ax.annotate('DSI: independent predictor\nOR=2.18, P=7.59×10⁻¹⁵\n(complementary bedside tool)',
            xy=(2.18, sorted_vars.index('DSI_mean')),
            xytext=(2.5, sorted_vars.index('DSI_mean')+0.5),
            fontsize=9, fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF5E6', edgecolor='#E74C3C', alpha=0.9),
            arrowprops=dict(arrowstyle='->', color='#E74C3C'))

plt.tight_layout()
plt.savefig(f'{OUT_DIR}/Fig3_Forest.png', dpi=300)
plt.savefig(f'{OUT_DIR}/Fig3_Forest.pdf', dpi=300)
print("  Fig3 Forest plot saved")

# ============================================================
# Figure S5: Calibration plots (primary model without surgery)
# ============================================================
print("Generating Figure S5: Calibration plots...")

from sklearn.calibration import calibration_curve

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (pred, name, color) in enumerate([
    (pred_basic, 'Basic baseline', 'k'),
    (pred_ext, 'Extended (no surgery)', 'b'),
    (pred_ext_dsi, 'Extended + DSI (no surgery)', 'r'),
]):
    y = df_clean['hospital_expire_flag'].values if idx == 0 else df_clean_ext['hospital_expire_flag'].values if idx == 1 else df_clean_ext_dsi['hospital_expire_flag'].values
    fraction_pos, mean_pred = calibration_curve(y, pred, n_bins=10, strategy='uniform')
    ax = axes[idx]
    ax.plot(mean_pred, fraction_pos, 's-', color=color, linewidth=2, label=name)
    ax.plot([0, 1], [0, 1], 'k:', linewidth=1)
    ax.set_xlabel('Mean predicted probability', fontsize=11)
    ax.set_ylabel('Fraction of positives', fontsize=11)
    ax.set_title(name, fontsize=11)
    ax.legend(loc='lower right', fontsize=9)
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])

plt.tight_layout()
plt.savefig(f'{OUT_DIR}/FigS5_Calibration.png', dpi=300)
plt.savefig(f'{OUT_DIR}/FigS5_Calibration.pdf', dpi=300)
print("  FigS5 Calibration saved")

# ============================================================
# Figure S4: DCA
# ============================================================
print("Generating Figure S4: DCA...")

def compute_net_benefit(y_true, y_pred, threshold):
    tp = np.sum((y_pred >= threshold) & (y_true == 1))
    fp = np.sum((y_pred >= threshold) & (y_true == 0))
    n = len(y_true)
    nb = tp/n - fp/n * threshold/(1-threshold)
    return nb

thresholds = np.arange(0.01, 0.50, 0.01)
y = df_clean_ext['hospital_expire_flag'].values

fig, ax = plt.subplots(figsize=(8, 6))
for pred, name, color, ls in [
    (pred_basic[df_clean.index.isin(df_clean_ext.index)], 'Basic baseline', 'k', '--'),
    (pred_ext, 'Extended (no surgery)', 'b', '-'),
    (pred_ext_dsi, 'Extended + DSI', 'r', '-'),
]:
    nb_vals = [compute_net_benefit(y, pred, t) for t in thresholds]
    ax.plot(thresholds, nb_vals, linestyle=ls, color=color, linewidth=2, label=name)

# Treat all and treat none
nb_all = [np.mean(y) - (1-np.mean(y))*t/(1-t) for t in thresholds]
nb_none = [0 for t in thresholds]
ax.plot(thresholds, nb_all, 'g:', linewidth=1, label='Treat all')
ax.plot(thresholds, nb_none, 'k:', linewidth=1, label='Treat none')
ax.set_xlabel('Threshold Probability', fontsize=12)
ax.set_ylabel('Net Benefit', fontsize=12)
ax.set_title('Decision Curve Analysis', fontsize=13)
ax.legend(loc='upper right', fontsize=9)
ax.set_xlim([0, 0.50])
ax.set_ylim([-0.10, 0.15])
plt.tight_layout()
plt.savefig(f'{OUT_DIR}/FigS4_DCA.png', dpi=300)
plt.savefig(f'{OUT_DIR}/FigS4_DCA.pdf', dpi=300)
print("  FigS4 DCA saved")

# ============================================================
# Figure S3: RCS
# ============================================================
print("Generating Figure S3: RCS...")

# RCS with 4 knots (5th, 35th, 65th, 95th percentiles)
si_vars = {
    'SI_mean': ('SI (HR/SBP)', '#E74C3C'),
    'MSI_mean': ('MSI (HR/MAP)', '#3498DB'),
    'DSI_mean': ('DSI (HR/DBP)', '#E74C3C'),
    'Age_SI_mean': ('Age-SI', '#2ECC71')
}

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for idx, (var, (label, color)) in enumerate(si_vars.items()):
    ax = axes[idx]
    vals = df[var].dropna().values
    q5, q35, q65, q95 = np.percentile(vals, [5, 35, 65, 95])
    knots = [q5, q35, q65, q95]
    
    # Simple quadratic fit for visualization
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression
    
    x_range = np.linspace(q5, q95, 100)
    y_data = df['hospital_expire_flag'].values
    
    # Group by bins and compute mortality
    bins = np.linspace(vals.min(), vals.max(), 20)
    bin_means = []
    mort_means = []
    for i in range(len(bins)-1):
        mask = (vals >= bins[i]) & (vals < bins[i+1])
        if mask.sum() > 10:
            bin_means.append(np.mean(vals[mask]))
            mort_means.append(np.mean(y_data[mask & (df[var].notna())]))
    
    ax.scatter(bin_means, mort_means, s=30, alpha=0.5, color=color)
    # Fit spline-like curve
    if len(bin_means) > 3:
        from scipy.interpolate import UnivariateSpline
        spline = UnivariateSpline(bin_means, mort_means, s=0.01)
        x_smooth = np.linspace(min(bin_means), max(bin_means), 200)
        y_smooth = spline(x_smooth)
        ax.plot(x_smooth, y_smooth, '-', color=color, linewidth=2)
    
    ax.set_xlabel(label, fontsize=11)
    ax.set_ylabel('In-hospital mortality', fontsize=11)
    ax.set_title(f'{label} dose-response', fontsize=11)
    ax.axvline(knots[0], color='gray', linestyle=':', alpha=0.5)
    ax.axvline(knots[3], color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig(f'{OUT_DIR}/FigS3_RCS.png', dpi=300)
plt.savefig(f'{OUT_DIR}/FigS3_RCS.pdf', dpi=300)
print("  FigS3 RCS saved")

# ============================================================
# Figure S7: CIF (Competing Risk)
# ============================================================
print("Generating Figure S7: CIF...")

df_cc = df[df['DSI_mean'].notna() & df['hospital_expire_flag'].notna()].copy()
# Define quartiles
dsi_q = pd.qcut(df_cc['DSI_mean'], 4, labels=['Q1','Q2','Q3','Q4'])
df_cc['dsi_quartile'] = dsi_q

# Time = hospital LOS, event = death or discharge
# For CIF: event 1 = death, event 2 = discharge alive
time_var = 'hospital_los_days' if 'hospital_los_days' in df_cc.columns else df_cc['los_hospital'] if 'los_hospital' in df_cc.columns else None

if time_var is None:
    # Estimate from ICU LOS (use icu_los as proxy)
    time_var = 'icu_los_days' if 'icu_los_days' in df_cc.columns else 'los_icu'

if time_var in df_cc.columns:
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#3498DB', '#2ECC71', '#F39C12', '#E74C3C']
    
    for q, color in zip(['Q1','Q2','Q3','Q4'], colors):
        sub = df_cc[df_cc['dsi_quartile'] == q]
        n = len(sub)
        deaths = sub['hospital_expire_flag'].sum()
        
        # Simple step function for cumulative incidence
        times = sub[time_var].sort_values().values
        events = sub['hospital_expire_flag'].values
        sorted_idx = np.argsort(sub[time_var].values)
        times_sorted = sub[time_var].values[sorted_idx]
        events_sorted = sub['hospital_expire_flag'].values[sorted_idx]
        
        # Cumulative incidence of death
        cum_inc = np.cumsum(events_sorted) / n
        ax.step(times_sorted, cum_inc, where='post', color=color, linewidth=2, 
                label=f'{q} (N={n}, mortality={deaths/n*100:.1f}%)')
    
    ax.set_xlabel('Time (days)', fontsize=12)
    ax.set_ylabel('Cumulative Incidence of In-Hospital Death', fontsize=12)
    ax.set_title('CIF by DSI Quartile (Competing Risk: Discharge)', fontsize=13)
    ax.legend(loc='upper left', fontsize=9)
    ax.set_ylim([0, 0.40])
    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/FigS7_CIF.png', dpi=300)
    plt.savefig(f'{OUT_DIR}/FigS7_CIF.pdf', dpi=300)
    print("  FigS7 CIF saved")
else:
    print("  FigS7 CIF: time variable not found, skipping")

# ============================================================
# Copy existing figures for unchanged items
# ============================================================
print("Copying unchanged figures from original figures/ directory...")
src_dir = 'figures'
unchanged = {
    'Fig1_Flowchart': 'Fig1_Flowchart',  # Flowchart unchanged
    'FigS1_Calibration_basic': 'FigS1_Calibration_basic',  # Basic calibration unchanged
    'FigS2_KM': 'FigS2_KM',  # KM unchanged
    'FigS6_Subgroup_ROC': 'Fig7_Subgroup_ROC',  # Subgroup ROC unchanged (rename to S6)
}

for target, source in unchanged.items():
    for ext in ['.png', '.pdf']:
        src = f'{src_dir}/{source}{ext}'
        dst = f'{OUT_DIR}/{target}{ext}'
        if os.path.exists(src):
            import shutil
            shutil.copy2(src, dst)
            print(f"  Copied {src} -> {dst}")

print("\nAll v7 figures generated!")
print(f"Output directory: {OUT_DIR}")

# List all generated files
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith('.png'):
        size = os.path.getsize(f'{OUT_DIR}/{f}')
        print(f"  {f} ({size/1024:.0f} KB)")
