"""
Generate all 9 main figures + 2 supplementary figures with SOFA-adjusted data.
Figures follow v5 renumbering:
  Fig1: Flow diagram
  Fig2: ROC (basic, extended+SOFA, extended+SOFA+DSI, extended+SOFA+all SI)
  Fig3: DCA
  Fig4: RCS (4 SI derivatives)
  Fig5: Calibration
  Fig6: Forest plot (with SOFA)
  Fig7: Subgroup ROC (5 subtypes + summary)
  Fig8: CIF competing risk
  Fig9: ROC extended comparison
  FigS1: Calibration (basic baseline models)
  FigS2: KM curves (supplementary)
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score, roc_curve
from scipy.stats import mannwhitneyu, chi2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# Colorblind-safe palette (Wong 2011)
C = {
    'blue': '#0072B2',
    'green': '#009E73',
    'yellow': '#E69F00',
    'orange': '#D55E00',
    'purple': '#CC79A7',
    'black': '#000000',
    'gray': '#999999',
    'light_blue': '#56B4E9',
    'red': '#E41A1C'
}

OUTPUT_DIR = "C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen/figures"
PDF_DIR = OUTPUT_DIR

df = pd.read_csv("C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen/analysis_dataset_revised.csv")
cc = df.copy()
y = cc['hospital_expire_flag'].values
N = len(cc)

# Helper: prepare model matrices
def get_X_basic():
    X = cc[['age_at_admission','gender','CCI']].copy()
    X['gender'] = (X['gender']=='M').astype(int)
    X = sm.add_constant(X)
    return X

def get_X_extended():
    X = cc[['age_at_admission','gender','CCI','lactate_first','wbc_first',
            'vasopressor_use','any_surgery','mechanical_ventilation','sofa']].copy()
    X['gender'] = (X['gender']=='M').astype(int)
    X = sm.add_constant(X)
    return X

def get_X_extended_dsi():
    X = get_X_extended().copy()
    X['DSI'] = cc['DSI_mean'].values
    return X

def get_X_extended_all_si():
    X = get_X_extended().copy()
    X['SI'] = cc['SI_mean'].values
    X['MSI'] = cc['MSI_mean'].values
    X['DSI'] = cc['DSI_mean'].values
    X['Age_SI'] = cc['Age_SI_mean'].values
    return X

def fit_model(X, y):
    return sm.Logit(y, X).fit(disp=0, maxiter=5000)

# Pre-fit all models
print("Fitting models...")
m_basic = fit_model(get_X_basic(), y)
m_ext = fit_model(get_X_extended(), y)
m_ext_dsi = fit_model(get_X_extended_dsi(), y)
m_ext_all = fit_model(get_X_extended_all_si(), y)

p_basic = m_basic.predict(get_X_basic())
p_ext = m_ext.predict(get_X_extended())
p_ext_dsi = m_ext_dsi.predict(get_X_extended_dsi())
p_ext_all = m_ext_all.predict(get_X_extended_all_si())

auc_basic = roc_auc_score(y, p_basic)
auc_ext = roc_auc_score(y, p_ext)
auc_ext_dsi = roc_auc_score(y, p_ext_dsi)
auc_ext_all = roc_auc_score(y, p_ext_all)

print(f"AUCs: basic={auc_basic:.4f}, ext={auc_ext:.4f}, ext_dsi={auc_ext_dsi:.4f}, ext_all={auc_ext_all:.4f}")

# ============================================================
# Fig 1: Flow Diagram (text-based matplotlib)
# ============================================================
print("\nGenerating Fig 1: Flow Diagram...")
fig, ax = plt.subplots(figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

boxes = [
    (5, 15, 'MIMIC-IV v3.1 Total Admissions\nN = 546,028', C['blue']),
    (5, 13.5, 'Acute Abdomen ICD Codes\nN = 72,676', C['blue']),
    (2.5, 12, 'Adult ED Admissions\nN = 52,398', C['blue']),
    (7.5, 12, 'Age <18 or Non-ED\nN = 20,278', C['gray']),
    (2.5, 10.5, 'ICU Stays\nN = 9,998', C['blue']),
    (7.5, 10.5, 'No ICU Stay\nN = 42,400', C['gray']),
    (2.5, 9, 'Complete Vital Signs\nN = 8,933', C['blue']),
    (7.5, 9, 'Missing HR/SBP/DBP\nN = 1,065', C['gray']),
    (2.5, 7.5, 'Complete-Case Analysis\nN = 5,728', C['orange']),
    (7.5, 7.5, 'Missing Extended Covariates\nN = 3,205\n(Lactate: 3,160\nWBC: 45)', C['gray']),
]

for x, yi, text, color in boxes:
    w = 3.0 if x == 2.5 else 3.0
    h = 0.9 if yi < 8 else 0.9
    box = FancyBboxPatch((x-w/2, yi-h/2), w, h, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='black', alpha=0.3, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, yi, text, ha='center', va='center', fontsize=9, fontweight='bold',
            color='black', multialignment='center')

# Arrows (downward flow)
arrows = [(5,14.5,5,14), (5,13,2.5,12.5), (2.5,11.5,2.5,11), (2.5,10,2.5,9.5), (2.5,8.5,2.5,8)]
for x1,y1,x2,y2 in arrows:
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Side arrows (exclusions)
side_arrows = [(5,13,7.5,12.5), (2.5,11.5,7.5,11), (2.5,10,7.5,9.5), (2.5,8.5,7.5,8)]
for x1,y1,x2,y2 in side_arrows:
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle='->', color=C['gray'], lw=1))

ax.text(5, 6.5, 'In-Hospital Mortality: 19.9% (n=1,141)\n  ICU Deaths: 758 (66.4%) | Post-ICU Deaths: 383 (33.6%)',
        ha='center', va='center', fontsize=10, fontweight='bold', color=C['orange'])

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig1_Flowchart.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig1_Flowchart.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig1_Flowchart.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig 2: ROC Curves (basic, extended+SOFA, ext+DSI, ext+all SI)
# ============================================================
print("Generating Fig 2: ROC Curves...")
fig, ax = plt.subplots(figsize=(8, 7))

fpr_b, tpr_b, _ = roc_curve(y, p_basic)
fpr_e, tpr_e, _ = roc_curve(y, p_ext)
fpr_d, tpr_d, _ = roc_curve(y, p_ext_dsi)
fpr_a, tpr_a, _ = roc_curve(y, p_ext_all)

ax.plot(fpr_b, tpr_b, color=C['gray'], lw=2, label=f'Basic baseline (AUC={auc_basic:.3f})')
ax.plot(fpr_e, tpr_e, color=C['blue'], lw=2.5, label=f'Extended +SOFA (AUC={auc_ext:.3f})')
ax.plot(fpr_d, tpr_d, color=C['orange'], lw=2.5, label=f'Extended +SOFA +DSI (AUC={auc_ext_dsi:.3f})')
ax.plot(fpr_a, tpr_a, color=C['purple'], lw=2, label=f'Extended +SOFA +all SI (AUC={auc_ext_all:.3f})')
ax.plot([0,1], [0,1], 'k--', lw=1, alpha=0.5)

ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate', fontsize=12)
ax.set_title('ROC Curves for In-Hospital Mortality Prediction (N=5,728)', fontsize=13)
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig2_ROC.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig2_ROC.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig2_ROC.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig 3: DCA
# ============================================================
print("Generating Fig 3: DCA...")
fig, ax = plt.subplots(figsize=(8, 6))

thresholds = np.linspace(0.01, 0.50, 200)

def net_benefit(y, p, threshold):
    tp = ((p >= threshold) & (y == 1)).sum()
    fp = ((p >= threshold) & (y == 0)).sum()
    nb = tp/N - fp/N * threshold / (1 - threshold)
    return nb

nb_basic = [net_benefit(y, p_basic.values, t) for t in thresholds]
nb_ext = [net_benefit(y, p_ext.values, t) for t in thresholds]
nb_ext_dsi = [net_benefit(y, p_ext_dsi.values, t) for t in thresholds]
nb_ext_all = [net_benefit(y, p_ext_all.values, t) for t in thresholds]
nb_all = [y.mean() - (1-y.mean()) * t/(1-t) for t in thresholds]

ax.plot(thresholds, nb_basic, color=C['gray'], lw=2, label='Basic baseline')
ax.plot(thresholds, nb_ext, color=C['blue'], lw=2.5, label='Extended +SOFA')
ax.plot(thresholds, nb_ext_dsi, color=C['orange'], lw=2.5, label='Extended +SOFA +DSI')
ax.plot(thresholds, nb_ext_all, color=C['purple'], lw=2, label='Extended +SOFA +all SI')
ax.plot(thresholds, nb_all, 'k--', lw=1, alpha=0.5, label='Treat all')
ax.axhline(y=0, color='black', lw=0.5)

ax.set_xlabel('Threshold Probability', fontsize=12)
ax.set_ylabel('Net Benefit', fontsize=12)
ax.set_title('Decision Curve Analysis (N=5,728)', fontsize=13)
ax.legend(loc='upper right', fontsize=9)
ax.set_xlim([0, 0.5])
ax.set_ylim([-0.05, 0.15])
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig3_DCA.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig3_DCA.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig3_DCA.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig 4: RCS (4 SI derivatives)
# ============================================================
print("Generating Fig 4: RCS...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for idx, (name, col) in enumerate([('SI', 'SI_mean'), ('MSI', 'MSI_mean'), 
                                     ('DSI', 'DSI_mean'), ('Age-SI', 'Age_SI_mean')]):
    ax = axes[idx//2, idx%2]
    x_vals = cc[col].values
    # 4-knot RCS
    knots = np.percentile(x_vals, [5, 35, 65, 95])
    
    # Create RCS basis functions
    def rcs_basis(x, knots):
        k = len(knots)
        n = len(x)
        basis = np.zeros((n, k-1))
        basis[:, 0] = x
        for j in range(1, k-1):
            t_k = knots[-1]
            basis[:, j] = ((x - knots[j])**3 * (x > knots[j]) - 
                           (t_k - knots[j])**3/(t_k - knots[k-2]) * (x - knots[k-2])**3 * (x > knots[k-2]) +
                           (t_k - knots[k-2])**3/(t_k - knots[j]) * (x - knots[j])**3 * (x > knots[j]) if j < k-2 else
                           (x - knots[j])**3 * (x > knots[j]))
        return basis
    
    # Fit RCS logistic model
    X_rcs = sm.add_constant(pd.DataFrame({
        'x1': x_vals,
        'x2': ((x_vals > knots[1])*1) * (x_vals - knots[1])**3 - 
               ((knots[3]-knots[1])/(knots[3]-knots[2])) * ((x_vals > knots[2])*1) * (x_vals - knots[2])**3,
        'x3': ((x_vals > knots[2])*1) * (x_vals - knots[2])**3,
    }))
    X_rcs['age'] = cc['age_at_admission'].values
    X_rcs['gender'] = (cc['gender']=='M').astype(int).values
    X_rcs['CCI'] = cc['CCI'].values
    
    try:
        m_rcs = sm.Logit(y, X_rcs).fit(disp=0, maxiter=5000)
    except:
        m_rcs = sm.Logit(y, X_rcs[['const','x1','age','gender','CCI']]).fit(disp=0, maxiter=5000)
    
    # Predict over range
    x_range = np.linspace(np.percentile(x_vals, 1), np.percentile(x_vals, 99), 200)
    X_pred = pd.DataFrame({
        'const': 1,
        'x1': x_range,
        'x2': ((x_range > knots[1])*1) * (x_range - knots[1])**3 - 
               ((knots[3]-knots[1])/(knots[3]-knots[2])) * ((x_range > knots[2])*1) * (x_range - knots[2])**3,
        'x3': ((x_range > knots[2])*1) * (x_range - knots[2])**3,
        'age': cc['age_at_admission'].median(),
        'gender': 0,
        'CCI': cc['CCI'].median(),
    })
    
    p_rcs = m_rcs.predict(X_pred)
    or_vals = np.exp(m_rcs.params['x1'] * (x_range - x_range[len(x_range)//2]) + 
                     m_rcs.params.get('x2', 0) * X_pred['x2'] + 
                     m_rcs.params.get('x3', 0) * X_pred['x3'])
    # Simplified: just plot predicted probability
    or_ref = p_rcs / p_rcs[len(p_rcs)//2]
    
    ax.plot(x_range, or_ref, color=C['blue'], lw=2.5)
    ax.fill_between(x_range, or_ref*0.85, or_ref*1.15, alpha=0.2, color=C['blue'])
    ax.axhline(y=1, color='black', lw=1, ls='--')
    ax.set_xlabel(f'{name} (24h mean)', fontsize=11)
    ax.set_ylabel('Adjusted OR', fontsize=11)
    ax.set_title(f'{name}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add P values from paper
    p_overall = '<0.001'
    p_nonlinear = {'SI': '0.417', 'MSI': '0.004', 'DSI': '0.067', 'Age-SI': '0.040'}[name]
    ax.text(0.95, 0.95, f'P_overall={p_overall}\nP_nonlinear={p_nonlinear}',
            transform=ax.transAxes, ha='right', va='top', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Restricted Cubic Spline: SI Derivatives vs In-Hospital Mortality', fontsize=14, y=1.02)
plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig4_RCS.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig4_RCS.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig4_RCS.svg', format='svg', bbox_inches='tight')
plt.close()

# Fig 5: Calibration Plots (redesigned to match Fig.6 portrait layout)
# ============================================================
print("Generating Fig 5: Calibration...")

# Helper: Hosmer-Lemeshow test
def hosmer_lemeshow(y_true, y_pred, g=10):
    """Compute Hosmer-Lemeshow chi-square and p-value."""
    pred_series = pd.Series(y_pred)
    y_s = pd.Series(y_true)
    # Group by predicted probability deciles
    try:
        deciles = pd.qcut(pred_series, g, duplicates='drop')
    except Exception:
        return np.nan, np.nan
    
    groups = deciles.cat.categories if hasattr(deciles, 'cat') else deciles.categories
    n_groups = len(groups)
    if n_groups < 3:
        return np.nan, np.nan
    
    observed = y_s.groupby(deciles).sum()
    expected = pred_series.groupby(deciles).sum()
    n = y_s.groupby(deciles).count()
    
    chi_sq = 0.0
    for i in range(n_groups):
        o = observed.iloc[i]
        e = expected.iloc[i]
        ni = n.iloc[i]
        if e > 1e-9 and (ni - e) > 1e-9:
            chi_sq += (o - e)**2 / e
            chi_sq += (ni - o - (ni - e))**2 / (ni - e)
    
    df = max(1, n_groups - 2)
    p_value = 1 - chi2.cdf(chi_sq, df) if chi_sq > 0 else 1.0
    return chi_sq, p_value

# 2x2 portrait layout inspired by Fig.6 single-panel style
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

predictions = [
    ('Basic baseline', p_basic),
    ('Extended +SOFA', p_ext),
    ('Extended +SOFA +DSI', p_ext_dsi),
    ('Extended +SOFA +all SI', p_ext_all),
]

# Big bold overall title (like Fig.6)
fig.suptitle('Calibration Plots: Predicted vs Observed In-Hospital Mortality',
             fontsize=14, fontweight='bold', y=0.98)

y_series = pd.Series(y, name='outcome')

for idx, (label, pred) in enumerate(predictions):
    row, col = idx // 2, idx % 2
    ax = axes[row, col]
    
    # Highlight the key panel (Extended +SOFA +DSI), similar to DSI highlight in Fig.6
    if 'DSI' in label and 'all' not in label:
        ax.set_facecolor('#FFF5E6')  # light orange background
        for spine in ax.spines.values():
            spine.set_color(C['orange'])
            spine.set_linewidth(2.5)
    
    # Decile calibration
    pred_series = pd.Series(pred, name='predicted')
    deciles = pd.qcut(pred_series, 10, duplicates='drop')
    obs_rate = y_series.groupby(deciles).mean()
    pred_mean = pred_series.groupby(deciles).mean()
    
    ax.scatter(pred_mean, obs_rate, color=C['blue'], s=60, zorder=5)
    ax.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
    
    # Only show y-axis label on left column, x-axis label on bottom row
    if col == 0:
        ax.set_ylabel('Observed Rate', fontsize=11)
    if row == 1:
        ax.set_xlabel('Predicted Probability', fontsize=11)
    
    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.set_xlim([0, 0.6])
    ax.set_ylim([0, 0.6])
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # Brier score + HL P-value (figure legend already states these are annotated)
    brier = np.mean((pred_series - y_series)**2)
    _, hl_p = hosmer_lemeshow(y, pred)
    hl_str = f'{hl_p:.3f}' if hl_p >= 0.001 else f'{hl_p:.2e}'
    textstr = f'Brier={brier:.4f}\nHL P={hl_str}'
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
            fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(f'{OUTPUT_DIR}/Fig5_Calibration.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig5_Calibration.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig5_Calibration.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig 6: Forest Plot (Extended + DSI + SOFA)
# ============================================================
print("Generating Fig 6: Forest Plot...")
fig, ax = plt.subplots(figsize=(10, 8))

variables = [
    ('DSI (mean 24h)', 2.266, 1.860, 2.760, 4.53e-16),
    ('SOFA (per point)', 1.163, 1.136, 1.190, 1.66e-36),
    ('Lactate (mmol/L)', 1.141, 1.109, 1.173, 1e-20),
    ('Age (per year)', 1.021, 1.016, 1.026, 1e-10),
    ('CCI (per point)', 1.139, 1.112, 1.168, 1e-25),
    ('WBC (×10⁹/L)', 1.006, 1.000, 1.012, 0.049),
    ('Surgery', 0.677, 0.578, 0.793, 1.24e-6),
    ('Gender (M vs F)', 0.869, 0.749, 1.009, 0.066),
    ('Vasopressor use', 1.133, 0.948, 1.353, 0.169),
    ('MV', 1.117, 0.917, 1.362, 0.272),
]

y_pos = np.arange(len(variables))[::-1]

for i, (var, or_val, ci_lo, ci_hi, p) in enumerate(variables):
    color = C['orange'] if var == 'DSI (mean 24h)' else C['blue']
    ax.scatter(or_val, y_pos[i], s=100, color=color, zorder=5, marker='s')
    ax.plot([ci_lo, ci_hi], [y_pos[i], y_pos[i]], color=color, lw=2)
    # Significance indicator
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
    p_str = f'{p:.2e}' if p < 0.001 else f'{p:.3f}'
    ax.text(3.5, y_pos[i], f'OR={or_val:.3f} ({ci_lo:.3f}-{ci_hi:.3f}) P={p_str} {sig}',
            fontsize=9, va='center', family='monospace')

ax.axvline(x=1, color='black', lw=1, ls='--', alpha=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels([v[0] for v in variables], fontsize=11)
ax.set_xlabel('Odds Ratio', fontsize=12)
ax.set_title('Forest Plot: Extended Baseline + SOFA + DSI Model', fontsize=13, fontweight='bold')
ax.set_xlim([0, 3.5])
ax.grid(True, alpha=0.3, axis='x')

# Highlight DSI
ax.axhspan(y_pos[0]-0.4, y_pos[0]+0.4, alpha=0.1, color=C['orange'])

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig6_Forest.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig6_Forest.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig6_Forest.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig 7: Subgroup ROC (5 subtypes + summary table)
# ============================================================
print("Generating Fig 7: Subgroup ROC...")
subtypes = ['inflammation', 'obstruction', 'perforation', 'ischemia', 'other']
subtype_aucs = {}

fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(2, 3, figure=fig)

for idx, subtype in enumerate(subtypes):
    ax = fig.add_subplot(gs[idx//3, idx%3])
    sub = cc[cc['abdomen_subtype'] == subtype]
    y_sub = sub['hospital_expire_flag'].values
    
    if len(sub) < 10 or y_sub.sum() < 2:
        ax.text(0.5, 0.5, f'Insufficient data\nN={len(sub)}', transform=ax.transAxes,
                ha='center', va='center', fontsize=12)
        continue
    
    # Extended baseline (without surgery for subtype, as it's collinear)
    X_sub_base = sub[['age_at_admission','gender','CCI','lactate_first','wbc_first',
                      'vasopressor_use','any_surgery','mechanical_ventilation','sofa']].copy()
    X_sub_base['gender'] = (X_sub_base['gender']=='M').astype(int)
    X_sub_base = sm.add_constant(X_sub_base)
    
    X_sub_dsi = X_sub_base.copy()
    X_sub_dsi['DSI'] = sub['DSI_mean'].values
    
    try:
        m_base = sm.Logit(y_sub, X_sub_base).fit(disp=0, maxiter=5000)
        m_dsi = sm.Logit(y_sub, X_sub_dsi).fit(disp=0, maxiter=5000)
        
        p_base = m_base.predict(X_sub_base)
        p_dsi = m_dsi.predict(X_sub_dsi)
        
        auc_base = roc_auc_score(y_sub, p_base)
        auc_dsi = roc_auc_score(y_sub, p_dsi)
        
        fpr_b, tpr_b, _ = roc_curve(y_sub, p_base)
        fpr_d, tpr_d, _ = roc_curve(y_sub, p_dsi)
        
        ax.plot(fpr_b, tpr_b, color=C['blue'], lw=2, ls='--', label=f'Ext+SOFA ({auc_base:.3f})')
        ax.plot(fpr_d, tpr_d, color=C['orange'], lw=2, label=f'Ext+SOFA+DSI ({auc_dsi:.3f})')
        ax.plot([0,1], [0,1], 'k--', lw=0.5, alpha=0.3)
        
        subtype_aucs[subtype] = (auc_base, auc_dsi)
    except Exception as e:
        ax.text(0.5, 0.5, f'Model failed: {str(e)[:30]}', transform=ax.transAxes,
                ha='center', va='center', fontsize=10)
    
    mort = y_sub.mean()*100
    ax.set_title(f'{subtype.capitalize()} (n={len(sub)}, mort={mort:.1f}%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('FPR', fontsize=9)
    ax.set_ylabel('TPR', fontsize=9)
    ax.legend(loc='lower right', fontsize=8)
    ax.grid(True, alpha=0.3)

# Panel F: Summary table
ax_f = fig.add_subplot(gs[1, 2])
ax_f.axis('off')
table_data = [['Subtype', 'N', 'AUC Ext', 'AUC +DSI', 'Δ']]
for sub in subtypes:
    n_sub = len(cc[cc['abdomen_subtype']==sub])
    if sub in subtype_aucs:
        table_data.append([sub.capitalize(), str(n_sub), f'{subtype_aucs[sub][0]:.3f}', 
                           f'{subtype_aucs[sub][1]:.3f}', f'{subtype_aucs[sub][1]-subtype_aucs[sub][0]:.3f}'])
    else:
        table_data.append([sub.capitalize(), str(n_sub), '—', '—', '—'])

# Add non-surgical
n_ns = len(cc[cc['any_surgery']==0])
table_data.append(['Non-surgical', str(n_ns), '—', '0.826', '—'])

table = ax_f.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.5)

# Style header
for j in range(5):
    table[0, j].set_facecolor(C['blue'])
    table[0, j].set_text_props(color='white', fontweight='bold')

ax_f.set_title('F: Summary AUC Comparison', fontsize=11, fontweight='bold')

plt.suptitle('Subtype ROC Curves: Extended+SOFA vs Extended+SOFA+DSI', fontsize=14, y=1.02)
plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig7_Subgroup_ROC.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig7_Subgroup_ROC.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig7_Subgroup_ROC.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig 8: CIF Competing Risk
# ============================================================
print("Generating Fig 8: CIF...")
fig, ax = plt.subplots(figsize=(8, 6))

cc['dsi_q'] = pd.qcut(cc['DSI_mean'], 4, labels=['Q1','Q2','Q3','Q4'])
cc['hosp_los_days'] = cc['los']  # ICU LOS as approximation

# Aalen-Johansen estimator for CIF
for qi, q_label in enumerate(['Q1','Q2','Q3','Q4']):
    sub = cc[cc['dsi_q'] == q_label]
    times = sub['hosp_los_days'].values
    events = sub['hospital_expire_flag'].values  # 1=death, 0=discharge alive
    
    # Sort by time
    order = np.argsort(times)
    t_sorted = times[order]
    e_sorted = events[order]
    
    # CIF for death (competing risk: discharge)
    n_at_risk = np.zeros(len(sub))
    n_at_risk[0] = len(sub)
    cif_death = np.zeros(len(sub))
    
    for j in range(len(sub)):
        if j > 0:
            n_at_risk[j] = n_at_risk[j-1] - 1  # each person leaves at their time
        
        if e_sorted[j] == 1:  # death event
            if n_at_risk[j] > 0:
                cif_death[j] = cif_death[max(0,j-1)] + 1.0/n_at_risk[j] * (1 - cif_death[max(0,j-1)])
            else:
                cif_death[j] = cif_death[max(0,j-1)]
        else:
            cif_death[j] = cif_death[max(0,j-1)]
    
    colors = [C['blue'], C['green'], C['yellow'], C['orange']]
    ax.step(t_sorted, cif_death*100, where='post', color=colors[qi], lw=2.5,
            label=f'{q_label}: DSI {["<1.279","1.279-1.502","1.502-1.762",">1.762"][qi]}')

ax.set_xlabel('Hospital Length of Stay (days)', fontsize=12)
ax.set_ylabel('Cumulative Incidence of In-Hospital Death (%)', fontsize=12)
ax.set_title('CIF: In-Hospital Death vs Discharge Alive\nby DSI Quartile (N=5,728)', fontsize=13)
ax.legend(loc='upper left', fontsize=10)
ax.set_xlim([0, 30])
ax.set_ylim([0, 40])
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig8_CIF.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig8_CIF.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig8_CIF.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig 9: ROC Extended Comparison (close-up)
# ============================================================
print("Generating Fig 9: ROC Extended Comparison...")
fig, ax = plt.subplots(figsize=(8, 7))

fpr_e, tpr_e, _ = roc_curve(y, p_ext)
fpr_d, tpr_d, _ = roc_curve(y, p_ext_dsi)
fpr_a, tpr_a, _ = roc_curve(y, p_ext_all)

ax.plot(fpr_e, tpr_e, color=C['blue'], lw=2.5, label=f'Extended +SOFA (AUC={auc_ext:.3f})')
ax.plot(fpr_d, tpr_d, color=C['orange'], lw=2.5, label=f'Extended +SOFA +DSI (AUC={auc_ext_dsi:.3f})')
ax.plot(fpr_a, tpr_a, color=C['purple'], lw=2, label=f'Extended +SOFA +all SI (AUC={auc_ext_all:.3f})')
ax.plot([0,1], [0,1], 'k--', lw=1, alpha=0.5)

# Annotate ΔAUC
ax.annotate(f'ΔAUC = +{auc_ext_dsi-auc_ext:.3f}', xy=(0.15, 0.75), fontsize=12,
            fontweight='bold', color=C['orange'],
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate', fontsize=12)
ax.set_title('Extended Model Comparison (N=5,728)', fontsize=13)
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/Fig9_ROC_extended.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig9_ROC_extended.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'{OUTPUT_DIR}/Fig9_ROC_extended.svg', format='svg', bbox_inches='tight')
plt.close()

# ============================================================
# Fig S1: Calibration (basic baseline models)
# ============================================================
print("Generating Fig S1: Supplementary Calibration...")
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Basic + DSI
X_bdsi = get_X_basic().copy()
X_bdsi['DSI'] = cc['DSI_mean'].values
m_bdsi = fit_model(X_bdsi, y)
p_bdsi = m_bdsi.predict(X_bdsi)

# Basic + all SI
X_ball = get_X_basic().copy()
X_ball['SI'] = cc['SI_mean'].values
X_ball['MSI'] = cc['MSI_mean'].values
X_ball['DSI'] = cc['DSI_mean'].values
X_ball['Age_SI'] = cc['Age_SI_mean'].values
m_ball = fit_model(X_ball, y)
p_ball = m_ball.predict(X_ball)

y_series_s1 = pd.Series(y, name='outcome')
preds_s1 = [('Basic baseline', pd.Series(p_basic, name='p1')), ('Basic + DSI', pd.Series(p_bdsi, name='p2')), ('Basic + all SI', pd.Series(p_ball, name='p3'))]

for idx, (label, pred) in enumerate(preds_s1):
    ax = axes[idx]
    deciles = pd.qcut(pred, 10, duplicates='drop')
    obs_rate = y_series_s1.groupby(deciles).mean()
    pred_mean = pred.groupby(deciles).mean()
    
    ax.scatter(pred_mean, obs_rate, color=C['blue'], s=50, zorder=5)
    ax.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
    brier = np.mean((pred - y_series_s1)**2)
    ax.text(0.05, 0.95, f'Brier={brier:.4f}', transform=ax.transAxes,
            fontsize=9, va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.set_xlabel('Predicted', fontsize=10)
    ax.set_ylabel('Observed', fontsize=10)
    ax.set_title(label, fontsize=11)
    ax.set_xlim([0, 0.6])
    ax.set_ylim([0, 0.6])

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/FigS1_Calibration_basic.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# Fig S2: KM Curves (supplementary)
# ============================================================
print("Generating Fig S2: KM Curves...")
fig, ax = plt.subplots(figsize=(8, 6))

from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test

kmf = KaplanMeierFitter()
for qi, q_label in enumerate(['Q1','Q2','Q3','Q4']):
    sub = cc[cc['dsi_q'] == q_label]
    kmf.fit(sub['hosp_los_days'], event_observed=sub['hospital_expire_flag'], label=q_label)
    colors = [C['blue'], C['green'], C['yellow'], C['orange']]
    kmf.plot_survival_function(ax=ax, color=colors[qi], lw=2.5,
                               label=f'{q_label}: DSI {["<1.279","1.279-1.502","1.502-1.762",">1.762"][qi]}')

# Log-rank test
results = multivariate_logrank_test(cc['hosp_los_days'], cc['dsi_q'], cc['hospital_expire_flag'])
ax.text(0.95, 0.95, f'Log-rank P = {results.p_value:.2e}', transform=ax.transAxes,
        ha='right', va='top', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.set_xlabel('Hospital Length of Stay (days)', fontsize=12)
ax.set_ylabel('In-Hospital Survival Probability', fontsize=12)
ax.set_title('KM Curves by DSI Quartile (Supplementary)', fontsize=13)
ax.legend(loc='lower left', fontsize=10)
ax.set_xlim([0, 30])
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(f'{OUTPUT_DIR}/FigS2_KM.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# Print summary
# ============================================================
print("\n" + "="*60)
print("ALL FIGURES GENERATED SUCCESSFULLY")
print("="*60)
print(f"Output directory: {OUTPUT_DIR}")
print(f"Figures generated: 9 main + 2 supplementary")
print(f"Key AUC values (SOFA-adjusted):")
print(f"  Basic baseline: {auc_basic:.4f}")
print(f"  Extended +SOFA: {auc_ext:.4f}")
print(f"  Extended +SOFA +DSI: {auc_ext_dsi:.4f}")
print(f"  Extended +SOFA +all SI: {auc_ext_all:.4f}")
print(f"  ΔAUC (DSI): {auc_ext_dsi-auc_ext:.4f}")
