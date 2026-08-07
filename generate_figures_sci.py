"""
SCI-Quality Figure Generation Script
=====================================
Generates all 10 figures at publication quality:
  Fig.1  - Patient Selection Flowchart (matplotlib rendering of draw.io layout)
  Fig.2  - ROC Curves (4 models)
  Fig.3  - Decision Curve Analysis
  Fig.4  - Restricted Cubic Splines (2x2)
  Fig.5  - Kaplan-Meier Survival (with number-at-risk)
  Fig.6  - Calibration Plot
  Fig.7  - Forest Plot (table-style)
  Fig.8  - Subgroup ROC (2x3)
  Fig.9  - Cumulative Incidence Function
  Fig.10 - ROC Extended (incremental value)

Design standards:
  - Lancet-inspired color palette (colorblind-friendly)
  - Font: DejaVu Sans (Arial substitute), sizes per journal conventions
  - Single column: 89 mm (3.5"), Double column: 178 mm (7.0")
  - 300 DPI PNG + vector PDF
  - Panel labels (A, B, C, D) for multi-panel figures
  - No overlapping elements
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from scipy import stats
from scipy.stats import norm
from sklearn.metrics import roc_curve, auc
import statsmodels.api as sm
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# GLOBAL SCI SETTINGS
# ============================================================
DPI = 300
FIG_DIR = 'figures_sci'
os.makedirs(FIG_DIR, exist_ok=True)

# Lancet-inspired color palette (colorblind-friendly)
C = {
    'blue':    '#005AAB',  # Lancet blue
    'red':     '#C0392B',  # Brick red
    'green':   '#00A651',  # Emerald
    'purple':  '#7D3C98',  # Royal purple
    'orange':  '#E67E22',  # Burnt orange
    'gray':    '#7F8C8D',  # Slate gray
    'dark':    '#2C3E50',  # Dark navy
    'q1':      '#2ECC71',  # Light green
    'q2':      '#3498DB',  # Light blue
    'q3':      '#F39C12',  # Amber
    'q4':      '#E74C3C',  # Red
}

# Model colors
MODEL_COLORS = {
    'basic':  C['gray'],
    'ext':    C['red'],
    'dsi':    C['green'],
    'all':    C['purple'],
}

# Font and style settings
plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'font.size':          8,
    'axes.titlesize':     9,
    'axes.labelsize':     8,
    'xtick.labelsize':    7,
    'ytick.labelsize':    7,
    'legend.fontsize':    7,
    'figure.dpi':         DPI,
    'savefig.dpi':        DPI,
    'savefig.bbox':       'tight',
    'savefig.pad_inches': 0.05,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.linewidth':     0.6,
    'xtick.major.width':  0.5,
    'ytick.major.width':  0.5,
    'xtick.major.size':   3,
    'ytick.major.size':   3,
    'grid.linewidth':     0.4,
    'lines.linewidth':    1.5,
})

# Figure size constants (inches)
W_SINGLE = 3.54   # 90 mm single column
W_DOUBLE = 7.09   # 180 mm double column
W_ONEHALF = 5.51  # 140 mm 1.5 column

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv('analysis_dataset_corrected.csv')
df['gender_male'] = (df['gender'] == 'M').astype(int)

model_vars_base = ['age_at_admission', 'gender_male', 'CCI']
model_vars_ext  = ['lactate_first', 'wbc_first', 'vasopressor_use', 'any_surgery', 'mechanical_ventilation']
si_vars = ['SI_mean', 'MSI_mean', 'DSI_mean', 'Age_SI_mean']
outcome_col = 'hospital_expire_flag'
all_vars = model_vars_base + model_vars_ext + si_vars + [outcome_col]

df_cc = df[all_vars].dropna().copy()
df_cc['abdomen_subtype'] = df.loc[df_cc.index, 'abdomen_subtype']
df_cc['los'] = df.loc[df_cc.index, 'los']
df_cc['icu_death_strict'] = df.loc[df_cc.index, 'icu_death_strict']

print(f"CC: {len(df_cc)}, Mortality: {df_cc[outcome_col].mean()*100:.1f}%")

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def fit_logistic(X, y):
    X = sm.add_constant(X, has_constant='add')
    return sm.Logit(y, X).fit(disp=0, method='lbfgs', maxiter=500)

def compute_auc(y_true, y_pred):
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    auc_val = auc(fpr, tpr)
    # Bootstrap CI
    aucs = []
    for _ in range(1000):
        idx = np.random.choice(len(y_true), len(y_true), replace=True)
        if y_true[idx].sum() > 0 and (1 - y_true[idx]).sum() > 0:
            fpr_b, tpr_b, _ = roc_curve(y_true[idx], y_pred[idx])
            aucs.append(auc(fpr_b, tpr_b))
    ci_lo = np.percentile(aucs, 2.5)
    ci_hi = np.percentile(aucs, 97.5)
    return auc_val, ci_lo, ci_hi, fpr, tpr

def rcs_transform(x, knots):
    x = np.array(x, dtype=float)
    k = len(knots)
    basis = [x.copy()]
    for j in range(2, k):
        def _h(xx, kj, kl):
            return (np.maximum(0, (xx - kj)**3)
                    - np.maximum(0, (xx - kl)**3) * (kl - knots[j-1]) / (kl - knots[j-2])
                    + np.maximum(0, (xx - knots[j-2])**3) * (kl - kj) / (kl - knots[j-2]))
        basis.append(_h(x, knots[j-1], knots[-1]))
    return np.column_stack(basis)

def add_panel_label(ax, label, x=-0.08, y=1.05):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=10, fontweight='bold',
            va='top', ha='left')

def fmt_p(p):
    if p < 0.001:
        return 'P < 0.001'
    elif p < 0.01:
        return f'P = {p:.3f}'
    else:
        return f'P = {p:.2f}'

def save_fig(fig, name):
    fig.savefig(os.path.join(FIG_DIR, f'{name}.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, f'{name}.pdf'))
    plt.close(fig)
    print(f'  {name} saved.')

# ============================================================
# FIG 1: FLOWCHART (matplotlib high-quality rendering)
# ============================================================
def generate_fig1():
    fig, ax = plt.subplots(1, 1, figsize=(W_SINGLE, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Layout
    main_x = 0.8
    main_w = 4.5
    main_cx = main_x + main_w / 2
    excl_x = 6.2
    excl_w = 2.8
    excl_cx = excl_x + excl_w / 2
    arrow_gap = 0.35

    main_heights = [0.95, 1.25, 0.70, 0.95, 1.25, 1.55]
    exclude_heights = [0.85, 0.70, 0.95]

    y_pos = [10.3]
    for i in range(1, len(main_heights)):
        y_pos.append(y_pos[i-1] - main_heights[i-1]/2 - arrow_gap - main_heights[i]/2)

    final_w = 5.0
    final_x = main_cx - final_w / 2

    main_texts = [
        ('MIMIC-IV v3.1 Database\nN = 546,028 hospital admissions\n(2008\u20132022)', True, '#DAE8FC', '#6C8EBF', 1.5),
        ('Acute abdomen ICD codes\n(K35\u2013K38, K80\u2013K83, K85\u2013K86,\nK56, K65, K55, K57, etc.)\nN = 72,676 admissions', False, '#DAE8FC', '#6C8EBF', 1.2),
        ('Acute abdomen ICU patients\nN = 8,933 ICU stays', False, '#DAE8FC', '#6C8EBF', 1.2),
        ('Complete vital signs data\n(HR, SBP, DBP, MAP in 24h)\nN = 8,933', False, '#DAE8FC', '#6C8EBF', 1.2),
        ('Extended covariates available\n(Lactate, WBC, Vasopressor,\nSurgery, Mechanical ventilation)\nN = 8,933', False, '#DAE8FC', '#6C8EBF', 1.2),
        ('Complete-case analysis cohort\nN = 5,728\nIn-hospital mortality: 19.9% (1,141)\nStrict ICU mortality: 13.2% (758)', True, '#D5E8D4', '#82B366', 2.0),
    ]
    exclude_texts = [
        'Excluded:\nNon-ICU admissions\n(n = 63,743)',
        'Excluded:\nAge < 18 (n = 0)\nInvalid vitals (n = 0)',
        'Excluded:\nMissing SI derivatives\nor extended covariates\n(n = 3,205)',
    ]
    exclude_indices = [1, 2, 4]

    # Draw main boxes
    for i, (y, h, (text, bold, fc, ec, lw)) in enumerate(zip(y_pos, main_heights, main_texts)):
        w = final_w if i == len(y_pos) - 1 else main_w
        x = final_x if i == len(y_pos) - 1 else main_x
        box = mpatches.FancyBboxPatch(
            (x, y - h/2), w, h,
            boxstyle='round,pad=0.03,rounding_size=0.12',
            facecolor=fc, edgecolor=ec, linewidth=lw
        )
        ax.add_patch(box)
        fw = 'bold' if bold else 'normal'
        ax.text(x + w/2, y, text, ha='center', va='center', fontsize=7.5,
                fontweight=fw, linespacing=1.15)

    # Draw exclusion boxes
    for idx, h, text in zip(exclude_indices, exclude_heights, exclude_texts):
        y_main = y_pos[idx]
        box = mpatches.FancyBboxPatch(
            (excl_x, y_main - h/2), excl_w, h,
            boxstyle='round,pad=0.03,rounding_size=0.10',
            facecolor='#F8CECC', edgecolor='#B85450', linewidth=1.0
        )
        ax.add_patch(box)
        ax.text(excl_cx, y_main, text, ha='center', va='center', fontsize=7,
                color='#B85450', linespacing=1.10)

    # Vertical arrows
    for i in range(len(y_pos) - 1):
        y_top = y_pos[i] - main_heights[i] / 2
        y_bot = y_pos[i+1] + main_heights[i+1] / 2
        ax.annotate('', xy=(main_cx, y_bot), xytext=(main_cx, y_top),
                    arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.2))

    # Horizontal arrows
    for idx in exclude_indices:
        y_main = y_pos[idx]
        x_start = main_x + main_w
        x_end = excl_x
        ax.annotate('', xy=(x_end, y_main), xytext=(x_start, y_main),
                    arrowprops=dict(arrowstyle='->', color='#B85450', lw=0.8))

    ax.set_title('Figure 1. Patient Selection Flowchart', fontsize=9, fontweight='bold', pad=8)
    save_fig(fig, 'Fig1_Flowchart')


# ============================================================
# FIG 2: ROC COMPARISON
# ============================================================
def generate_fig2():
    y = df_cc[outcome_col].values

    X_base = df_cc[model_vars_base].values
    m_base = fit_logistic(X_base, y)
    p_base = m_base.predict(sm.add_constant(X_base))
    auc_b, lo_b, hi_b, fpr_b, tpr_b = compute_auc(y, p_base)

    X_ext = df_cc[model_vars_base + model_vars_ext].values
    m_ext = fit_logistic(X_ext, y)
    p_ext = m_ext.predict(sm.add_constant(X_ext))
    auc_e, lo_e, hi_e, fpr_e, tpr_e = compute_auc(y, p_ext)

    X_dsi = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values
    m_dsi = fit_logistic(X_dsi, y)
    p_dsi = m_dsi.predict(sm.add_constant(X_dsi))
    auc_d, lo_d, hi_d, fpr_d, tpr_d = compute_auc(y, p_dsi)

    X_all = df_cc[model_vars_base + model_vars_ext + si_vars].values
    m_all = fit_logistic(X_all, y)
    p_all = m_all.predict(sm.add_constant(X_all))
    auc_a, lo_a, hi_a, fpr_a, tpr_a = compute_auc(y, p_all)

    fig, ax = plt.subplots(1, 1, figsize=(W_SINGLE, W_SINGLE * 0.85))

    ax.plot(fpr_b, tpr_b, color=MODEL_COLORS['basic'], lw=1.2, ls=':',
            label=f'Basic baseline (AUC={auc_b:.3f})')
    ax.plot(fpr_e, tpr_e, color=MODEL_COLORS['ext'], lw=1.8,
            label=f'Extended baseline (AUC={auc_e:.3f} [{lo_e:.3f}\u2013{hi_e:.3f}])')
    ax.plot(fpr_d, tpr_d, color=MODEL_COLORS['dsi'], lw=2.2,
            label=f'Extended + DSI (AUC={auc_d:.3f} [{lo_d:.3f}\u2013{hi_d:.3f}])')
    ax.plot(fpr_a, tpr_a, color=MODEL_COLORS['all'], lw=1.2, ls='--',
            label=f'Extended + all SI (AUC={auc_a:.3f} [{lo_a:.3f}\u2013{hi_a:.3f}])')

    ax.plot([0, 1], [0, 1], 'k--', lw=0.5, alpha=0.4)
    ax.set_xlabel('1 \u2013 Specificity')
    ax.set_ylabel('Sensitivity')
    ax.legend(loc='lower right', framealpha=0.95, edgecolor='#CCCCCC')
    ax.set_xlim([-0.01, 1.01])
    ax.set_ylim([-0.01, 1.01])
    ax.grid(True, alpha=0.15, linewidth=0.3)

    fig.tight_layout()
    save_fig(fig, 'Fig2_ROC')

    return {
        '_model_base': m_base, '_model_ext': m_ext,
        '_model_dsi': m_dsi, '_model_all': m_all,
        'auc_basic': (auc_b, lo_b, hi_b),
        'auc_ext': (auc_e, lo_e, hi_e),
        'auc_dsi': (auc_d, lo_d, hi_d),
        'auc_all': (auc_a, lo_a, hi_a),
    }


# ============================================================
# FIG 3: DCA
# ============================================================
def generate_fig3(auc_results):
    y = df_cc[outcome_col].values

    X_base = df_cc[model_vars_base].values
    p_base = auc_results['_model_base'].predict(sm.add_constant(X_base))
    X_ext = df_cc[model_vars_base + model_vars_ext].values
    p_ext = auc_results['_model_ext'].predict(sm.add_constant(X_ext))
    X_dsi = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values
    p_dsi = auc_results['_model_dsi'].predict(sm.add_constant(X_dsi))

    threshold = np.arange(0.05, 0.50, 0.005)
    prevalence = y.mean()

    fig, ax = plt.subplots(1, 1, figsize=(W_SINGLE, W_SINGLE * 0.85))

    for name, pred, color, ls, lw in [
        ('Basic baseline', p_base, MODEL_COLORS['basic'], '-', 1.2),
        ('Extended baseline', p_ext, MODEL_COLORS['ext'], '-', 1.5),
        ('Extended + DSI', p_dsi, MODEL_COLORS['dsi'], '-', 2.0),
    ]:
        nb = []
        for pt in threshold:
            tp = np.sum((pred >= pt) & (y == 1))
            fp = np.sum((pred >= pt) & (y == 0))
            n = len(y)
            nb.append(tp / n - fp / n * pt / (1 - pt))
        ax.plot(threshold, nb, color=color, lw=lw, ls=ls, label=name)

    treat_all = prevalence - (1 - prevalence) * threshold / (1 - threshold)
    ax.plot(threshold, treat_all, color=C['gray'], lw=0.8, ls='--', alpha=0.6, label='Treat all')
    ax.axhline(y=0, color=C['gray'], lw=0.5, ls=':', alpha=0.5)

    ax.set_xlabel('Threshold Probability')
    ax.set_ylabel('Net Benefit')
    ax.legend(loc='upper right', framealpha=0.95, edgecolor='#CCCCCC')
    ax.set_xlim([0.05, 0.45])
    ax.set_ylim([-0.02, 0.10])
    ax.grid(True, alpha=0.15, linewidth=0.3)

    fig.tight_layout()
    save_fig(fig, 'Fig3_DCA')


# ============================================================
# FIG 4: RCS (2x2)
# ============================================================
def generate_fig4():
    y = df_cc[outcome_col].values
    fig, axes = plt.subplots(2, 2, figsize=(W_DOUBLE, W_DOUBLE * 0.65))
    axes = axes.flatten()

    si_items = [
        ('SI',     'SI_mean',     C['blue'],   'SI = HR/SBP'),
        ('MSI',    'MSI_mean',    C['red'],    'MSI = HR/MAP'),
        ('DSI',    'DSI_mean',    C['green'],  'DSI = HR/DBP'),
        ('Age-SI', 'Age_SI_mean', C['purple'], 'Age-SI = SI\u00d7Age/10'),
    ]
    panel_labels = ['A', 'B', 'C', 'D']

    for idx, (si_name, si_col, color, formula) in enumerate(si_items):
        ax = axes[idx]
        x_data = df_cc[si_col].values
        x_clean = x_data[(x_data > np.percentile(x_data, 1)) & (x_data < np.percentile(x_data, 99))]
        knots = np.percentile(x_clean, [5, 35, 65, 95])

        rcs_basis = rcs_transform(x_data, knots)
        n_basis = rcs_basis.shape[1]

        X_rcs = np.column_stack([rcs_basis, df_cc['age_at_admission'].values,
                                  df_cc['gender_male'].values, df_cc['CCI'].values])
        model = fit_logistic(X_rcs, y)

        x_range = np.linspace(np.percentile(x_data, 1), np.percentile(x_data, 99), 200)
        rcs_range = rcs_transform(x_range, knots)
        n_pred = len(x_range)
        X_pred = np.column_stack([rcs_range,
                                   np.full(n_pred, df_cc['age_at_admission'].median()),
                                   np.full(n_pred, df_cc['gender_male'].median()),
                                   np.full(n_pred, df_cc['CCI'].median())])
        pred = model.predict(sm.add_constant(X_pred, has_constant='add'))

        ref = y.mean()
        ax.plot(x_range, pred, color=color, lw=1.8)
        ax.axhline(y=ref, color=C['gray'], ls=':', lw=0.8, alpha=0.6)

        # Nonlinearity test
        X_lin = np.column_stack([x_data, df_cc['age_at_admission'].values,
                                  df_cc['gender_male'].values, df_cc['CCI'].values])
        m_lin = fit_logistic(X_lin, y)
        X_cov = np.column_stack([df_cc['age_at_admission'].values,
                                  df_cc['gender_male'].values, df_cc['CCI'].values])
        m_cov = fit_logistic(X_cov, y)
        lr_nonlin = -2 * (m_lin.llf - model.llf)
        p_nonlin = stats.chi2.sf(lr_nonlin, n_basis - 1)
        lr_total = -2 * (m_cov.llf - model.llf)
        p_overall = stats.chi2.sf(lr_total, n_basis)

        p_text = f'{fmt_p(p_overall)}\nP nonlinearity = {p_nonlin:.3f}'
        ax.text(0.03, 0.97, p_text, transform=ax.transAxes, fontsize=7,
                va='top', ha='left',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.95,
                          edgecolor='#CCCCCC', linewidth=0.5))

        ax.set_xlabel(si_name, fontsize=8)
        ax.set_ylabel('Predicted Probability', fontsize=7)
        ax.set_title(formula, fontsize=8, fontweight='bold')
        add_panel_label(ax, panel_labels[idx], x=-0.06, y=1.02)
        ax.grid(True, alpha=0.12, linewidth=0.3)

        y_min = max(0, pred.min() - 0.05)
        y_max = min(0.5, pred.max() + 0.05)
        if y_max - y_min < 0.10:
            y_min = max(0, ref - 0.10)
            y_max = min(0.5, ref + 0.10)
        ax.set_ylim([y_min, y_max])

    fig.suptitle('Figure 4. Restricted Cubic Spline Analysis of SI Derivatives\n'
                 '(4-knot RCS, adjusted for age, sex, CCI)',
                 fontsize=9, fontweight='bold', y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save_fig(fig, 'Fig4_RCS')


# ============================================================
# FIG 5: KAPLAN-MEIER (with number-at-risk)
# ============================================================
def generate_fig5():
    from lifelines.statistics import multivariate_logrank_test

    df_km = df_cc.copy()
    df_km['time'] = df.loc[df_km.index, 'los']
    df_km['event'] = df_km[outcome_col]
    df_km['DSI_Q'] = pd.qcut(df_km['DSI_mean'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

    fig, ax = plt.subplots(1, 1, figsize=(W_SINGLE, W_SINGLE * 1.05))

    q_colors = [C['q1'], C['q2'], C['q3'], C['q4']]
    q_labels = ['Q1 (lowest DSI)', 'Q2', 'Q3', 'Q4 (highest DSI)']
    max_t = 30
    time_points = [0, 5, 10, 15, 20, 25, 30]

    km_data = {}
    for q, color, label in zip(['Q1', 'Q2', 'Q3', 'Q4'], q_colors, q_labels):
        q_data = df_km[df_km['DSI_Q'] == q]
        times = q_data['time'].values
        events = q_data['event'].values
        sort_idx = np.argsort(times)
        times_s = times[sort_idx]
        events_s = events[sort_idx]

        unique_t = np.unique(times_s)
        s_curr = 1.0
        s_times = [0]
        survival = [1.0]
        for t in unique_t:
            n_risk = np.sum(times_s >= t)
            d = np.sum((times_s == t) & (events_s == 1))
            if n_risk > 0 and d > 0:
                s_curr *= (1 - d / n_risk)
            s_times.append(t)
            survival.append(s_curr)

        ax.step(s_times, survival, where='post', color=color, lw=1.5, label=label)
        km_data[q] = (times_s, events_s)

    # Log-rank test
    result = multivariate_logrank_test(df_km['time'], df_km['DSI_Q'], df_km['event'])
    p_val = result.p_value
    ax.text(0.97, 0.97, f'Log-rank {fmt_p(p_val)}', transform=ax.transAxes,
            fontsize=7, va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.95,
                      edgecolor='#CCCCCC', linewidth=0.5))

    ax.set_xlabel('Hospital Length of Stay (days)')
    ax.set_ylabel('In-Hospital Survival Probability')
    ax.legend(loc='lower left', framealpha=0.95, edgecolor='#CCCCCC')
    ax.set_xlim([0, max_t])
    ax.set_ylim([0.55, 1.02])
    ax.grid(True, alpha=0.15, linewidth=0.3)

    # Number at risk table
    risk_ax = ax.inset_axes([0, -0.22, 1, 0.12])
    risk_ax.set_xlim(0, max_t)
    risk_ax.set_ylim(-0.5, 3.5)
    risk_ax.axis('off')
    risk_ax.text(-0.5, 1.5, 'No. at risk', fontsize=6, ha='right', va='center',
                 transform=risk_ax.transData)

    for i, (q, color) in enumerate(zip(['Q1', 'Q2', 'Q3', 'Q4'], q_colors)):
        times_s, events_s = km_data[q]
        row_y = 3 - i
        risk_ax.text(-0.5, row_y, q, fontsize=6, ha='right', va='center',
                     color=color, transform=risk_ax.transData)
        for tp in time_points:
            n_risk = np.sum(times_s > tp)
            risk_ax.text(tp, row_y, str(n_risk), fontsize=6, ha='center', va='center')

    # Column headers for time points
    for tp in time_points:
        risk_ax.text(tp, 3.8, str(tp), fontsize=6, ha='center', va='bottom')

    fig.tight_layout()
    save_fig(fig, 'Fig5_KM')


# ============================================================
# FIG 6: CALIBRATION
# ============================================================
def generate_fig6(auc_results):
    y = df_cc[outcome_col].values
    models_data = [
        ('Basic baseline', auc_results['_model_base'].predict(
            sm.add_constant(df_cc[model_vars_base].values)), MODEL_COLORS['basic']),
        ('Extended baseline', auc_results['_model_ext'].predict(
            sm.add_constant(df_cc[model_vars_base + model_vars_ext].values)), MODEL_COLORS['ext']),
        ('Extended + DSI', auc_results['_model_dsi'].predict(
            sm.add_constant(df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values)),
            MODEL_COLORS['dsi']),
        ('Extended + all SI', auc_results['_model_all'].predict(
            sm.add_constant(df_cc[model_vars_base + model_vars_ext + si_vars].values)),
            MODEL_COLORS['all']),
    ]

    fig, ax = plt.subplots(1, 1, figsize=(W_SINGLE, W_SINGLE * 0.95))

    n_groups = 10
    for name, pred, color in models_data:
        quantiles = np.percentile(pred, np.linspace(0, 100, n_groups + 1))
        obs, prd = [], []
        for i in range(n_groups):
            mask = (pred >= quantiles[i]) & (pred < quantiles[i + 1])
            if mask.sum() > 0:
                obs.append(y[mask].mean())
                prd.append(pred[mask].mean())
        ax.plot(prd, obs, 'o-', color=color, lw=1.5, markersize=4, label=name)

    ax.plot([0, 0.5], [0, 0.5], 'k--', lw=0.6, alpha=0.5, label='Perfect calibration')

    ax.set_xlabel('Predicted Probability')
    ax.set_ylabel('Observed Probability')
    ax.legend(loc='lower right', framealpha=0.95, edgecolor='#CCCCCC')
    ax.set_xlim([0, 0.5])
    ax.set_ylim([0, 0.5])
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.15, linewidth=0.3)

    fig.tight_layout()
    save_fig(fig, 'Fig6_Calibration')


# ============================================================
# FIG 7: FOREST PLOT (table-style)
# ============================================================
def generate_fig7(auc_results):
    model = auc_results['_model_dsi']
    params = model.params
    conf = model.conf_int()
    if isinstance(conf, pd.DataFrame):
        conf_arr = conf.values
    else:
        conf_arr = conf

    var_labels = [
        'Age (per year)', 'Male sex', 'CCI',
        'Lactate (mmol/L)', 'WBC (\u00d710\u2079/L)',
        'Vasopressor use', 'Surgery', 'Mechanical ventilation',
        'DSI (HR/DBP)',
    ]
    n_vars = len(var_labels)

    ors = np.exp(params[1:n_vars + 1])
    ci_lo = np.exp(conf_arr[1:n_vars + 1, 0])
    ci_hi = np.exp(conf_arr[1:n_vars + 1, 1])
    pvals = model.pvalues[1:n_vars + 1]

    sort_idx = np.argsort(np.abs(np.log(ors)))[::-1]

    fig, ax = plt.subplots(1, 1, figsize=(W_DOUBLE, W_DOUBLE * 0.45))

    y_pos = np.arange(n_vars)
    for i, idx in enumerate(sort_idx):
        or_val = float(ors[idx])
        lo = float(ci_lo[idx])
        hi = float(ci_hi[idx])
        p = float(pvals[idx])

        marker = C['red'] if p < 0.05 else C['gray']
        ax.errorbar(or_val, i, xerr=[[or_val - lo], [hi - or_val]],
                    fmt='o', color=C['dark'], ecolor=C['gray'],
                    elinewidth=1.5, capsize=3, markersize=6,
                    markerfacecolor=marker, markeredgecolor=C['dark'], zorder=3)

        p_str = 'P<0.001' if p < 0.001 else f'P={p:.3f}'
        ax.text(hi + 0.15, i, f'{or_val:.2f} ({lo:.2f}\u2013{hi:.2f})  {p_str}',
                fontsize=7, va='center', ha='left')

    ax.axvline(x=1, color=C['gray'], ls='--', lw=0.8, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([var_labels[sort_idx[i]] for i in range(n_vars)], fontsize=8)
    ax.set_xlabel('Odds Ratio (95% CI)', fontsize=8)
    ax.grid(True, alpha=0.12, linewidth=0.3, axis='x')
    ax.set_xlim([0, max(float(ci_hi.max()) * 1.8, 4.5)])
    ax.invert_yaxis()

    # Remove top/right spines already off; add light left spine
    ax.spines['left'].set_linewidth(0.6)
    ax.spines['bottom'].set_linewidth(0.6)

    fig.tight_layout()
    save_fig(fig, 'Fig7_Forest')


# ============================================================
# FIG 8: SUBGROUP ROC (2x3)
# ============================================================
def generate_fig8():
    subtypes = ['inflammation', 'obstruction', 'perforation', 'ischemia', 'other']
    subtype_colors = {
        'inflammation': C['blue'], 'obstruction': C['red'],
        'perforation': C['green'], 'ischemia': C['purple'],
        'other': C['orange'],
    }

    fig, axes = plt.subplots(2, 3, figsize=(W_DOUBLE, W_DOUBLE * 0.60))
    axes_flat = axes.flatten()
    panel_labels = ['A', 'B', 'C', 'D', 'E']

    for idx, subtype in enumerate(subtypes):
        ax = axes_flat[idx]
        sub = df_cc[df_cc['abdomen_subtype'] == subtype].copy()

        if len(sub) < 30 or sub[outcome_col].sum() < 5:
            ax.text(0.5, 0.5, f'{subtype}\nInsufficient events',
                    ha='center', va='center', fontsize=8, transform=ax.transAxes)
            ax.set_title(f'{subtype.capitalize()}', fontsize=8)
            continue

        y_sub = sub[outcome_col].values
        X_sub = sub[model_vars_base + model_vars_ext + ['DSI_mean']].values
        try:
            X_c = sm.add_constant(X_sub, has_constant='add')
            m_sub = sm.Logit(y_sub, X_c).fit(disp=0, method='lbfgs', maxiter=500)
            pred = m_sub.predict(X_c)
            auc_sub, ci_lo, ci_hi, fpr, tpr = compute_auc(y_sub, pred)
            ax.plot(fpr, tpr, color=subtype_colors.get(subtype, C['dark']), lw=1.8,
                    label=f'Ext+DSI\nAUC={auc_sub:.3f}\n[{ci_lo:.3f}\u2013{ci_hi:.3f}]')
        except Exception:
            ax.text(0.5, 0.5, f'{subtype}\nModel failed', ha='center', va='center',
                    fontsize=8, transform=ax.transAxes)
            ax.set_title(f'{subtype.capitalize()}', fontsize=8)
            continue

        # Extended baseline
        X_ext = sub[model_vars_base + model_vars_ext].values
        try:
            X_c2 = sm.add_constant(X_ext, has_constant='add')
            m_ext = sm.Logit(y_sub, X_c2).fit(disp=0, method='lbfgs', maxiter=500)
            pred_e = m_ext.predict(X_c2)
            auc_e, _, _, fpr_e, tpr_e = compute_auc(y_sub, pred_e)
            ax.plot(fpr_e, tpr_e, color=C['gray'], lw=1.0, ls='--',
                    label=f'Ext baseline\nAUC={auc_e:.3f}')
        except Exception:
            pass

        ax.plot([0, 1], [0, 1], 'k--', lw=0.4, alpha=0.3)
        ax.set_xlabel('1 \u2013 Specificity', fontsize=7)
        ax.set_ylabel('Sensitivity', fontsize=7)
        n_d = int(sub[outcome_col].sum())
        ax.set_title(f'{subtype.capitalize()} (n={len(sub)}, death={n_d})', fontsize=8)
        ax.legend(fontsize=6, loc='lower right', framealpha=0.9, edgecolor='#CCCCCC')
        ax.set_xlim([-0.01, 1.01])
        ax.set_ylim([-0.01, 1.01])
        ax.grid(True, alpha=0.12, linewidth=0.3)
        add_panel_label(ax, panel_labels[idx], x=-0.08, y=1.02)

    # Summary panel (6th)
    ax_sum = axes_flat[5]
    ax_sum.axis('off')
    summary_data = []
    for st in subtypes:
        sub = df_cc[df_cc['abdomen_subtype'] == st]
        n = len(sub)
        d = int(sub[outcome_col].sum())
        mort = sub[outcome_col].mean() * 100
        summary_data.append((st.capitalize(), n, d, f'{mort:.1f}%'))

    col_labels = ['Subtype', 'N', 'Deaths', 'Mortality']
    table = ax_sum.table(cellText=[[s, n, d, m] for s, n, d, m in summary_data],
                         colLabels=col_labels, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1, 1.4)
    for (r, c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor('#E8E8E8')
            cell.set_text_props(fontweight='bold')
        else:
            cell.set_facecolor('#FFFFFF' if r % 2 == 0 else '#F8F8F8')
        cell.set_edgecolor('#CCCCCC')
        cell.set_linewidth(0.3)
    add_panel_label(ax_sum, 'F', x=-0.05, y=0.95)

    fig.suptitle('Figure 8. Subgroup ROC Analysis by Acute Abdomen Subtype',
                 fontsize=9, fontweight='bold', y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save_fig(fig, 'Fig8_Subgroup_ROC')


# ============================================================
# FIG 9: CIF (Competing Risk)
# ============================================================
def generate_fig9():
    df_cif = df_cc.copy()
    df_cif['time'] = df.loc[df_cif.index, 'los']
    df_cif['DSI_Q'] = pd.qcut(df_cif['DSI_mean'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

    fig, ax = plt.subplots(1, 1, figsize=(W_SINGLE, W_SINGLE * 0.95))

    q_colors = [C['q1'], C['q2'], C['q3'], C['q4']]
    q_labels = ['Q1 (lowest DSI)', 'Q2', 'Q3', 'Q4 (highest DSI)']

    for q, color, label in zip(['Q1', 'Q2', 'Q3', 'Q4'], q_colors, q_labels):
        q_data = df_cif[df_cif['DSI_Q'] == q]
        times = q_data['time'].values
        events = q_data[outcome_col].values

        sort_idx = np.argsort(times)
        t_s = times[sort_idx]
        e_s = events[sort_idx]

        unique_t = np.unique(t_s)
        cif_cum = 0.0
        S_overall = 1.0
        cif_times = [0]
        cif_vals = [0]

        for t_k in unique_t:
            n_risk = np.sum(t_s >= t_k)
            d_primary = np.sum((t_s == t_k) & (e_s == 1))
            d_all = np.sum(t_s == t_k)
            if n_risk > 0:
                increment = (d_primary / n_risk) * S_overall
                cif_cum += increment
                S_overall *= (1 - d_all / n_risk)
            cif_times.append(t_k)
            cif_vals.append(min(cif_cum, 0.40))

        ax.step(cif_times, cif_vals, where='post', color=color, lw=1.5, label=label)

    ax.set_xlabel('Hospital Length of Stay (days)')
    ax.set_ylabel('Cumulative Incidence of In-Hospital Death')
    ax.legend(loc='upper left', framealpha=0.95, edgecolor='#CCCCCC')
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 0.40])
    ax.grid(True, alpha=0.15, linewidth=0.3)

    fig.tight_layout()
    save_fig(fig, 'Fig9_CIF')


# ============================================================
# FIG 10: ROC EXTENDED (incremental value)
# ============================================================
def generate_fig10(auc_results):
    y = df_cc[outcome_col].values

    X_base = df_cc[model_vars_base].values
    p_base = auc_results['_model_base'].predict(sm.add_constant(X_base))
    auc_b, _, _, fpr_b, tpr_b = compute_auc(y, p_base)

    X_ext = df_cc[model_vars_base + model_vars_ext].values
    p_ext = auc_results['_model_ext'].predict(sm.add_constant(X_ext))
    auc_e, lo_e, hi_e, fpr_e, tpr_e = compute_auc(y, p_ext)

    X_dsi = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values
    p_dsi = auc_results['_model_dsi'].predict(sm.add_constant(X_dsi))
    auc_d, lo_d, hi_d, fpr_d, tpr_d = compute_auc(y, p_dsi)

    X_all = df_cc[model_vars_base + model_vars_ext + si_vars].values
    p_all = auc_results['_model_all'].predict(sm.add_constant(X_all))
    auc_a, lo_a, hi_a, fpr_a, tpr_a = compute_auc(y, p_all)

    fig, ax = plt.subplots(1, 1, figsize=(W_SINGLE, W_SINGLE * 0.85))

    ax.plot(fpr_b, tpr_b, color=MODEL_COLORS['basic'], lw=1.0, ls=':',
            label=f'Basic baseline (AUC={auc_b:.3f})')
    ax.plot(fpr_e, tpr_e, color=MODEL_COLORS['ext'], lw=1.5,
            label=f'Extended baseline (AUC={auc_e:.3f} [{lo_e:.3f}\u2013{hi_e:.3f}])')
    ax.plot(fpr_d, tpr_d, color=MODEL_COLORS['dsi'], lw=2.0,
            label=f'Extended + DSI (AUC={auc_d:.3f} [{lo_d:.3f}\u2013{hi_d:.3f}])')
    ax.plot(fpr_a, tpr_a, color=MODEL_COLORS['all'], lw=1.0, ls='--',
            label=f'Extended + all SI (AUC={auc_a:.3f} [{lo_a:.3f}\u2013{hi_a:.3f}])')

    ax.plot([0, 1], [0, 1], 'k--', lw=0.4, alpha=0.3)
    ax.set_xlabel('1 \u2013 Specificity')
    ax.set_ylabel('Sensitivity')
    ax.legend(loc='lower right', framealpha=0.95, edgecolor='#CCCCCC')
    ax.set_xlim([-0.01, 1.01])
    ax.set_ylim([-0.01, 1.01])
    ax.grid(True, alpha=0.15, linewidth=0.3)

    # Annotate incremental value
    ax.annotate(f'\u0394AUC = {auc_d - auc_e:.3f}',
                xy=(0.35, 0.80), fontsize=7, color=C['green'],
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9,
                          edgecolor=C['green'], linewidth=0.5))

    fig.tight_layout()
    save_fig(fig, 'Fig10_ROC_extended')


# ============================================================
# MAIN
# ============================================================
print('=' * 60)
print('SCI-Quality Figure Generation')
print(f'CC: {len(df_cc)}, Mortality: {df_cc[outcome_col].mean()*100:.1f}%')
print(f'Output: {FIG_DIR}/')
print('=' * 60)

print('\n[1/10] Fig1 Flowchart...')
generate_fig1()

print('[2/10] Fig2 ROC...')
auc_results = generate_fig2()

print('[3/10] Fig3 DCA...')
generate_fig3(auc_results)

print('[4/10] Fig4 RCS...')
generate_fig4()

print('[5/10] Fig5 KM...')
generate_fig5()

print('[6/10] Fig6 Calibration...')
generate_fig6(auc_results)

print('[7/10] Fig7 Forest...')
generate_fig7(auc_results)

print('[8/10] Fig8 Subgroup ROC...')
generate_fig8()

print('[9/10] Fig9 CIF...')
generate_fig9()

print('[10/10] Fig10 ROC Extended...')
generate_fig10(auc_results)

print('\n' + '=' * 60)
print(f'All 10 figures generated in {FIG_DIR}/')
print('=' * 60)
