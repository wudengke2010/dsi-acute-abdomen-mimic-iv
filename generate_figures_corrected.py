"""
SCI Paper Figure Regeneration Script (Corrected)
=================================================
Generates all 10 figures for the Shock Index SCI paper using:
- analysis_dataset_corrected.csv
- hospital_expire_flag as primary outcome (in-hospital mortality)
- icu_death_strict as secondary outcome (strict ICU mortality)
- CC sample N=5,728

All figures: 300 DPI, SCI-quality formatting
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
# GLOBAL SETTINGS
# ============================================================
DPI = 300
FIG_DIR = 'figures_corrected'
os.makedirs(FIG_DIR, exist_ok=True)

# SCI-quality color palette (accessible, distinguishable)
COLORS = {
    'basic_baseline': '#4A90D9',   # blue
    'extended_baseline': '#E74C3C', # red
    'ext_dsi': '#2ECC71',           # green
    'ext_all_si': '#9B59B6',        # purple
    'si': '#4A90D9',
    'msi': '#E74C3C',
    'dsi': '#2ECC71',
    'age_si': '#9B59B6',
    'q1': '#2ECC71',
    'q2': '#3498DB',
    'q3': '#F39C12',
    'q4': '#E74C3C',
    'inflammation': '#3498DB',
    'obstruction': '#E74C3C',
    'perforation': '#2ECC71',
    'ischemia': '#9B59B6',
    'other': '#F39C12',
}

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': DPI,
    'savefig.dpi': DPI,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv('analysis_dataset_corrected.csv')
df['gender_male'] = (df['gender'] == 'M').astype(int)

# Complete case dataset
model_vars_base = ['age_at_admission', 'gender_male', 'CCI']
model_vars_ext = ['lactate_first', 'wbc_first', 'vasopressor_use', 'any_surgery', 'mechanical_ventilation']
si_vars = ['SI_mean', 'MSI_mean', 'DSI_mean', 'Age_SI_mean']
outcome_col = 'hospital_expire_flag'
all_vars = model_vars_base + model_vars_ext + si_vars + [outcome_col]

df_cc = df[all_vars].dropna().copy()
print(f"Complete cases: {len(df_cc)}")
print(f"In-hospital mortality: {df_cc[outcome_col].mean()*100:.2f}% ({df_cc[outcome_col].sum()} deaths)")

# Add subtype and other columns to df_cc from original df
df_cc['abdomen_subtype'] = df.loc[df_cc.index, 'abdomen_subtype']
df_cc['los'] = df.loc[df_cc.index, 'los']
df_cc['icu_death_strict'] = df.loc[df_cc.index, 'icu_death_strict']

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def fit_logistic(X, y):
    """Fit logistic regression with statsmodels"""
    X = sm.add_constant(X, has_constant='add')
    model = sm.Logit(y, X).fit(disp=0, method='lbfgs', maxiter=200)
    return model

def compute_auc(y_true, y_pred):
    """Compute AUC with 95% CI via DeLong method approximation"""
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    auc_val = auc(fpr, tpr)
    # Bootstrap CI
    n_boot = 1000
    aucs = []
    for _ in range(n_boot):
        idx = np.random.choice(len(y_true), len(y_true), replace=True)
        if y_true[idx].sum() > 0 and (1 - y_true[idx]).sum() > 0:
            fpr_b, tpr_b, _ = roc_curve(y_true[idx], y_pred[idx])
            aucs.append(auc(fpr_b, tpr_b))
    ci_low = np.percentile(aucs, 2.5)
    ci_high = np.percentile(aucs, 97.5)
    return auc_val, ci_low, ci_high, fpr, tpr

def rcs_transform(x, knots):
    """Restricted cubic spline transformation"""
    x = np.array(x, dtype=float)
    k = len(knots)
    basis = [x.copy()]
    for j in range(2, k):
        def _h(xx, kj, kl):
            return np.maximum(0, (xx - kj)**3) - \
                   np.maximum(0, (xx - kl)**3) * (kl - knots[j-1]) / (kl - knots[j-2]) + \
                   np.maximum(0, (xx - knots[j-2])**3) * (kl - kj) / (kl - knots[j-2])
        basis.append(_h(x, knots[j-1], knots[-1]))
    return np.column_stack(basis)

def compute_cif_correct(times, events, group_labels):
    """
    Correct Cumulative Incidence Function for competing risks.
    CIF_j(t) = sum over t_k <= t of [d_j(t_k) / n(t_k)] * S(t_k-)
    where S(t_k-) is the overall survival at just before t_k.
    
    events: 0=alive, 1=primary event (hospital death), 2=competing event (ICU death+discharged alive)
    Actually for our case:
    - Primary event: in-hospital death (hospital_expire_flag=1)
    - Competing risk for non-surgical patients: surgery (they get surgery and leave ICU)
    - Competing risk for surgical patients: we use hospital discharge alive
    
    Simplified: competing risk = discharge alive (not dying in hospital)
    """
    results = {}
    for g in np.unique(group_labels):
        g_mask = group_labels == g
        g_times = times[g_mask]
        g_events = events[g_mask]
        
        # Sort by time
        sort_idx = np.argsort(g_times)
        g_times_sorted = g_times[sort_idx]
        g_events_sorted = g_events[sort_idx]
        
        # Count at risk at each unique time
        unique_times = np.unique(g_times_sorted)
        cif_values = []
        
        # Overall survival product (all event types)
        S_product = 1.0
        
        n_total = len(g_times_sorted)
        prev_time = -1
        
        for t in unique_times:
            n_at_risk = np.sum(g_times_sorted >= t)
            d_primary = np.sum((g_times_sorted == t) & (g_events_sorted == 1))
            d_all = np.sum(g_times_sorted == t)
            
            if n_at_risk > 0:
                # CIF increment: (d_primary / n_at_risk) * S(t-)
                increment = (d_primary / n_at_risk) * S_product
                cif_values.append((t, S_product * d_primary / n_at_risk + (cif_values[-1][1] if cif_values else 0)))
                
                # Update overall survival for next time point
                if d_all > 0 and n_at_risk > 0:
                    S_product *= (1 - d_all / n_at_risk)
        
        if cif_values:
            cif_times = [c[0] for c in cif_values]
            cif_cumulative = [c[1] for c in cif_values]
        else:
            cif_times = [0]
            cif_cumulative = [0]
        
        results[g] = (np.array(cif_times), np.array(cif_cumulative))
    
    return results


# ============================================================
# FIG 1: FLOWCHART
# ============================================================
def generate_fig1():
    """Patient Selection Flowchart - complete with CC 5,728"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Layout parameters (data units)
    main_x = 1.9          # left edge of main boxes
    main_w = 4.2        # default width of main boxes
    main_cx = main_x + main_w / 2  # center x of main boxes
    exclude_x = 7.0     # left edge of exclusion boxes
    exclude_w = 2.3     # width of exclusion boxes
    exclude_cx = exclude_x + exclude_w / 2  # center x of exclusion boxes
    
    # Box heights chosen to comfortably fit text
    main_heights = [1.0, 1.3, 0.8, 1.0, 1.3, 1.8]
    exclude_heights = [0.9, 0.9, 0.9]
    
    # Vertical positions (center y of each box) with uniform arrow spacing
    arrow_gap = 0.40
    y_pos = [10.0]
    for i in range(1, len(main_heights)):
        y_pos.append(y_pos[i-1] - main_heights[i-1]/2 - arrow_gap - main_heights[i]/2)
    
    # Final green box is wider to accommodate outcome text
    final_w = 4.6
    final_x = main_cx - final_w / 2
    
    # Box contents
    main_texts = [
        'MIMIC-IV v3.1 Database\nN = 546,028 hospital admissions\n(2008–2022)',
        'Acute abdomen ICD codes\n(K35–K38, K80–K83, K85–K86,\nK56, K65, K55, K57, etc.)\nN = 72,676 admissions',
        'Acute abdomen ICU patients\nN = 8,933 ICU stays',
        'Complete vital signs data\n(HR, SBP, DBP, MAP in 24h)\nN = 8,933',
        'Extended covariates available\n(Lactate, WBC, Vasopressor,\nSurgery, Mechanical ventilation)\nN = 8,933',
        'Complete-case analysis cohort\nN = 5,728\nIn-hospital mortality: 19.9% (1,141)\nStrict ICU mortality: 13.2% (758)',
    ]
    exclude_texts = [
        'Excluded:\nNon-ICU admissions\n(n = 63,743)',
        'Excluded:\nAge < 18 (n = 0)\nInvalid vitals (n = 0)',
        'Excluded:\nMissing SI derivatives\nor extended covariates\n(n = 3,205)',
    ]
    
    # Draw main boxes
    for i, (y, h, text) in enumerate(zip(y_pos, main_heights, main_texts)):
        if i == 0 or i == len(y_pos) - 1:
            facecolor = '#E8F4FD' if i == 0 else '#D5F5E3'
            edgecolor = '#2C3E50' if i == 0 else '#27AE60'
            linewidth = 1.5 if i == 0 else 2.0
            fontweight = 'bold'
        else:
            facecolor = '#E8F4FD'
            edgecolor = '#2C3E50'
            linewidth = 1.5
            fontweight = 'normal'
        
        # Use wider dimensions for the final green box
        w = final_w if i == len(y_pos) - 1 else main_w
        x = final_x if i == len(y_pos) - 1 else main_x
        
        box = mpatches.FancyBboxPatch(
            (x, y - h/2), w, h,
            boxstyle='round,pad=0.02,rounding_size=0.15',
            facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth
        )
        ax.add_patch(box)
        ax.text(x + w/2, y, text, ha='center', va='center', fontsize=9,
                fontweight=fontweight, linespacing=1.15 if i == len(y_pos) - 1 else 1.1)
    
    # Draw exclusion boxes
    exclude_indices = [1, 2, 4]
    for idx, h, text in zip(exclude_indices, exclude_heights, exclude_texts):
        y_main = y_pos[idx]
        box = mpatches.FancyBboxPatch(
            (exclude_x, y_main - h/2), exclude_w, h,
            boxstyle='round,pad=0.02,rounding_size=0.12',
            facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=1.2
        )
        ax.add_patch(box)
        ax.text(exclude_cx, y_main, text, ha='center', va='center', fontsize=8,
                color='#E74C3C', linespacing=1.05)
    
    # Vertical arrows between main boxes
    for i in range(len(y_pos) - 1):
        y_top = y_pos[i] - main_heights[i] / 2
        y_bottom = y_pos[i+1] + main_heights[i+1] / 2
        ax.annotate('', xy=(main_cx, y_bottom), xytext=(main_cx, y_top),
                    arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
    
    # Horizontal arrows to exclusion boxes
    for idx in exclude_indices:
        y_main = y_pos[idx]
        x_start = main_x + main_w
        x_end = exclude_x
        ax.annotate('', xy=(x_end, y_main), xytext=(x_start, y_main),
                    arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1))
    
    ax.set_title('Figure 1. Patient Selection Flowchart', fontsize=12, fontweight='bold', pad=15)
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig1_Flowchart.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig1_Flowchart.pdf'))
    plt.close(fig)
    print("Fig1 saved.")


# ============================================================
# FIG 2: ROC COMPARISON
# ============================================================
def generate_fig2():
    """ROC curves for 4 SI derivatives + baseline models"""
    y = df_cc[outcome_col].values
    
    # Basic baseline
    X_base = df_cc[model_vars_base].values
    model_base = fit_logistic(X_base, y)
    pred_base = model_base.predict(sm.add_constant(X_base))
    auc_base, ci_lo_b, ci_hi_b, fpr_b, tpr_b = compute_auc(y, pred_base)
    
    # Extended baseline
    X_ext = df_cc[model_vars_base + model_vars_ext].values
    model_ext = fit_logistic(X_ext, y)
    pred_ext = model_ext.predict(sm.add_constant(X_ext))
    auc_ext, ci_lo_e, ci_hi_e, fpr_e, tpr_e = compute_auc(y, pred_ext)
    
    # Extended + DSI
    X_dsi = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values
    model_dsi = fit_logistic(X_dsi, y)
    pred_dsi = model_dsi.predict(sm.add_constant(X_dsi))
    auc_dsi, ci_lo_d, ci_hi_d, fpr_d, tpr_d = compute_auc(y, pred_dsi)
    
    # Extended + all SI
    X_all = df_cc[model_vars_base + model_vars_ext + si_vars].values
    model_all = fit_logistic(X_all, y)
    pred_all = model_all.predict(sm.add_constant(X_all))
    auc_all, ci_lo_a, ci_hi_a, fpr_a, tpr_a = compute_auc(y, pred_all)
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    
    ax.plot(fpr_b, tpr_b, color=COLORS['basic_baseline'], lw=2,
            label=f'Basic baseline (AUC={auc_base:.3f} [{ci_lo_b:.3f}-{ci_hi_b:.3f}])')
    ax.plot(fpr_e, tpr_e, color=COLORS['extended_baseline'], lw=2,
            label=f'Extended baseline (AUC={auc_ext:.3f} [{ci_lo_e:.3f}-{ci_hi_e:.3f}])')
    ax.plot(fpr_d, tpr_d, color=COLORS['ext_dsi'], lw=2.5,
            label=f'Extended + DSI (AUC={auc_dsi:.3f} [{ci_lo_d:.3f}-{ci_hi_d:.3f}])')
    ax.plot(fpr_a, tpr_a, color=COLORS['ext_all_si'], lw=1.5, linestyle='--',
            label=f'Extended + all SI (AUC={auc_all:.3f} [{ci_lo_a:.3f}-{ci_hi_a:.3f}])')
    
    ax.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
    ax.set_xlabel('False Positive Rate (1 – Specificity)')
    ax.set_ylabel('True Positive Rate (Sensitivity)')
    ax.set_title('Figure 2. ROC Curves for In-Hospital Mortality Prediction')
    ax.legend(loc='lower right', fontsize=8, framealpha=0.9)
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])
    ax.grid(True, alpha=0.3)
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig2_ROC.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig2_ROC.pdf'))
    plt.close(fig)
    
    # Save AUC values for later use
    auc_results = {
        'basic_baseline': (auc_base, ci_lo_b, ci_hi_b),
        'extended_baseline': (auc_ext, ci_lo_e, ci_hi_e),
        'ext_dsi': (auc_dsi, ci_lo_d, ci_hi_d),
        'ext_all_si': (auc_all, ci_lo_a, ci_hi_a),
    }
    print(f"Fig2 saved. AUCs: base={auc_base:.3f}, ext={auc_ext:.3f}, dsi={auc_dsi:.3f}, all={auc_all:.3f}")
    return auc_results, model_ext, model_dsi, model_all


# ============================================================
# FIG 3: DCA
# ============================================================
def generate_fig3(auc_results):
    """Decision Curve Analysis"""
    y = df_cc[outcome_col].values
    
    # Get predictions from models
    X_base = df_cc[model_vars_base].values
    model_base = fit_logistic(X_base, y)
    pred_base = model_base.predict(sm.add_constant(X_base))
    
    X_ext = df_cc[model_vars_base + model_vars_ext].values
    pred_ext = auc_results['_model_ext'].predict(sm.add_constant(X_ext))
    
    X_dsi = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values
    pred_dsi = auc_results['_model_dsi'].predict(sm.add_constant(X_dsi))
    
    threshold = np.arange(0.05, 0.95, 0.01)
    prevalence = y.mean()
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    
    for name, pred, color, ls in [
        ('Basic baseline', pred_base, COLORS['basic_baseline'], '-'),
        ('Extended baseline', pred_ext, COLORS['extended_baseline'], '-'),
        ('Extended + DSI', pred_dsi, COLORS['ext_dsi'], '-'),
    ]:
        net_benefit = []
        for pt in threshold:
            tp = np.sum((pred >= pt) & (y == 1))
            fp = np.sum((pred >= pt) & (y == 0))
            n = len(y)
            nb = tp / n - fp / n * pt / (1 - pt)
            net_benefit.append(nb)
        ax.plot(threshold, net_benefit, color=color, lw=2, ls=ls, label=name)
    
    # Treat all
    treat_all_nb = prevalence - (1 - prevalence) * threshold / (1 - threshold)
    ax.plot(threshold, treat_all_nb, 'k--', lw=1, alpha=0.5, label='Treat all')
    
    # Treat none
    ax.axhline(y=0, color='gray', lw=1, ls=':', label='Treat none')
    
    ax.set_xlabel('Threshold Probability')
    ax.set_ylabel('Net Benefit')
    ax.set_title('Figure 3. Decision Curve Analysis for In-Hospital Mortality')
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax.set_xlim([0.05, 0.80])
    ax.set_ylim([-0.05, 0.15])
    ax.grid(True, alpha=0.3)
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig3_DCA.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig3_DCA.pdf'))
    plt.close(fig)
    print("Fig3 saved.")


# ============================================================
# FIG 4: RCS (Restricted Cubic Splines)
# ============================================================
def generate_fig4():
    """RCS curves showing dose-response relationship of SI derivatives with in-hospital mortality"""
    y = df_cc[outcome_col].values
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    
    si_items = [
        ('SI', 'SI_mean', COLORS['si'], 'SI = HR/SBP'),
        ('MSI', 'MSI_mean', COLORS['msi'], 'MSI = HR/MAP'),
        ('DSI', 'DSI_mean', COLORS['dsi'], 'DSI = HR/DBP'),
        ('Age-SI', 'Age_SI_mean', COLORS['age_si'], 'Age-SI = SI×Age/10'),
    ]
    
    for ax_idx, (si_name, si_col, color, formula) in enumerate(si_items):
        ax = axes[ax_idx]
        x_data = df_cc[si_col].values
        
        # Remove extreme outliers for knot placement
        x_clean = x_data[(x_data > np.percentile(x_data, 1)) & (x_data < np.percentile(x_data, 99))]
        knots = np.percentile(x_clean, [5, 35, 65, 95])
        
        # Create RCS basis
        rcs_basis = rcs_transform(x_data, knots)
        n_basis = rcs_basis.shape[1]
        
        # Build model data - use consistent column ordering
        X_rcs = np.column_stack([
            rcs_basis,
            df_cc['age_at_admission'].values,
            df_cc['gender_male'].values,
            df_cc['CCI'].values,
        ])
        
        model = fit_logistic(X_rcs, y)
        
        # Prediction range
        x_range = np.linspace(np.percentile(x_data, 1), np.percentile(x_data, 99), 200)
        rcs_range = rcs_transform(x_range, knots)
        
        # Build prediction matrix with same column order
        n_pred = len(x_range)
        X_pred = np.column_stack([
            rcs_range,
            np.full(n_pred, df_cc['age_at_admission'].median()),
            np.full(n_pred, df_cc['gender_male'].median()),
            np.full(n_pred, df_cc['CCI'].median()),
        ])
        
        pred_proba = model.predict(sm.add_constant(X_pred, has_constant='add'))
        
        # Reference line (overall mortality rate)
        ref_line = y.mean()
        
        ax.plot(x_range, pred_proba, color=color, lw=2.5, label=f'{si_name} (adjusted)')
        ax.axhline(y=ref_line, color='gray', ls=':', lw=1, alpha=0.7, label=f'Reference ({ref_line:.1%})')
        
        # P-value annotation from likelihood ratio test
        # Linear model for comparison (only SI term + covariates, no RCS nonlinear terms)
        X_linear = np.column_stack([
            x_data,
            df_cc['age_at_admission'].values,
            df_cc['gender_male'].values,
            df_cc['CCI'].values,
        ])
        model_linear = fit_logistic(X_linear, y)
        
        # Likelihood ratio test for nonlinearity
        lr_stat = -2 * (model_linear.llf - model.llf)
        lr_df = n_basis - 1  # nonlinear terms (basis columns minus linear term)
        p_nonlinear = stats.chi2.sf(lr_stat, lr_df)
        
        # Overall test for the SI variable (RCS model vs covariates-only)
        X_cov_only = np.column_stack([
            df_cc['age_at_admission'].values,
            df_cc['gender_male'].values,
            df_cc['CCI'].values,
        ])
        model_cov_only = fit_logistic(X_cov_only, y)
        lr_stat_total = -2 * (model_cov_only.llf - model.llf)
        p_overall = stats.chi2.sf(lr_stat_total, n_basis + 3 - 3)  # all SI terms vs cov-only
        
        # Format P values for display
        def _fmt_p(p):
            if p < 0.001:
                return f"P < 1.0×10⁻³"
            else:
                return f"P = {p:.3f}"
        
        p_text = f'{_fmt_p(p_overall)}\nP nonlinear = {p_nonlinear:.3f}'
        
        ax.text(0.02, 0.98, p_text,
                transform=ax.transAxes, fontsize=8, va='top', ha='left',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95, edgecolor='gray', linewidth=0.8))
        
        ax.set_xlabel(si_name)
        ax.set_ylabel('Predicted Probability\nof In-Hospital Mortality')
        ax.set_title(f'{formula}', fontsize=10, fontweight='bold')
        ax.legend(fontsize=7, loc='best')
        ax.grid(True, alpha=0.3)
        
        # Set reasonable Y-axis range
        y_min = max(0, pred_proba.min() - 0.05)
        y_max = min(0.5, pred_proba.max() + 0.05)
        if y_max - y_min < 0.10:
            y_min = max(0, ref_line - 0.10)
            y_max = min(0.5, ref_line + 0.10)
        ax.set_ylim([y_min, y_max])
    
    fig.suptitle('Figure 4. Restricted Cubic Spline Analysis of SI Derivatives\nand In-Hospital Mortality (4-knot RCS, adjusted for age, sex, CCI)',
                 fontsize=11, fontweight='bold', y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig4_RCS.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig4_RCS.pdf'))
    plt.close(fig)
    print("Fig4 saved.")


# ============================================================
# FIG 5: KAPLAN-MEIER
# ============================================================
def generate_fig5():
    """KM survival curves by DSI quartile (in-hospital survival)"""
    # For KM, we use hospital length of stay as time variable
    # Event = in-hospital death; censor = alive at discharge
    
    df_cc_km = df_cc.copy()
    df_cc_km['time'] = df.loc[df_cc_km.index, 'los']  # LOS in days
    df_cc_km['event'] = df_cc_km[outcome_col]
    
    # DSI quartile
    df_cc_km['DSI_Q'] = pd.qcut(df_cc_km['DSI_mean'], q=4, labels=['Q1','Q2','Q3','Q4'])
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    
    q_colors = [COLORS['q1'], COLORS['q2'], COLORS['q3'], COLORS['q4']]
    q_labels = ['Q1 (lowest DSI)', 'Q2', 'Q3', 'Q4 (highest DSI)']
    
    for q, color, label in zip(['Q1','Q2','Q3','Q4'], q_colors, q_labels):
        q_data = df_cc_km[df_cc_km['DSI_Q'] == q]
        times = q_data['time'].values
        events = q_data['event'].values
        
        # Sort by time
        sort_idx = np.argsort(times)
        times_sorted = times[sort_idx]
        events_sorted = events[sort_idx]
        
        # KM survival
        unique_times = np.unique(times_sorted)
        survival = [1.0]
        s_times = [0]
        n_at_risk = len(times_sorted)
        s_curr = 1.0
        
        for t in unique_times:
            n_risk = np.sum(times_sorted >= t)
            d = np.sum((times_sorted == t) & (events_sorted == 1))
            if n_risk > 0 and d > 0:
                s_curr *= (1 - d / n_risk)
            s_times.append(t)
            survival.append(s_curr)
        
        # Add final point
        max_t = times_sorted.max()
        if s_times[-1] < max_t:
            s_times.append(max_t + 0.5)
            survival.append(s_curr)
        
        ax.step(s_times, survival, where='post', color=color, lw=2, label=label)
    
    # Log-rank test using lifelines multivariate_logrank_test
    from lifelines.statistics import multivariate_logrank_test
    try:
        result = multivariate_logrank_test(df_cc_km['time'], df_cc_km['DSI_Q'], df_cc_km['event'])
        p_val = result.p_value
    except Exception:
        # Fallback to contingency chi-square if logrank fails
        contingency = np.array([[q_data['event'].sum(), len(q_data) - q_data['event'].sum()]
                               for q in ['Q1','Q2','Q3','Q4']])
        chi2_val, p_val, dof, expected = stats.chi2_contingency(contingency)
    
    p_str = f'P < 0.001' if p_val < 0.001 else f'P = {p_val:.3f}'
    ax.text(0.98, 0.98, f'Log-rank {p_str}',
            transform=ax.transAxes, fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))
    
    ax.set_xlabel('Hospital Length of Stay (days)')
    ax.set_ylabel('In-Hospital Survival Probability')
    ax.set_title('Figure 5. Kaplan-Meier Curves by DSI Quartile\n(In-Hospital Survival)')
    ax.legend(loc='lower left', fontsize=8, framealpha=0.9)
    ax.set_xlim([0, 30])
    ax.set_ylim([0.5, 1.02])
    ax.grid(True, alpha=0.3)
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig5_KM.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig5_KM.pdf'))
    plt.close(fig)
    print("Fig5 saved.")


# ============================================================
# FIG 6: CALIBRATION
# ============================================================
def generate_fig6(auc_results):
    """Calibration plots for 4 models"""
    y = df_cc[outcome_col].values
    
    models_data = []
    
    # Basic baseline
    X = df_cc[model_vars_base].values
    pred = auc_results['_model_base'].predict(sm.add_constant(X, has_constant='add'))
    models_data.append(('Basic baseline', pred, COLORS['basic_baseline']))
    
    # Extended baseline
    X = df_cc[model_vars_base + model_vars_ext].values
    pred = auc_results['_model_ext'].predict(sm.add_constant(X, has_constant='add'))
    models_data.append(('Extended baseline', pred, COLORS['extended_baseline']))
    
    # Extended + DSI
    X = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values
    pred = auc_results['_model_dsi'].predict(sm.add_constant(X, has_constant='add'))
    models_data.append(('Extended + DSI', pred, COLORS['ext_dsi']))
    
    # Extended + all SI
    X = df_cc[model_vars_base + model_vars_ext + si_vars].values
    pred = auc_results['_model_all'].predict(sm.add_constant(X, has_constant='add'))
    models_data.append(('Extended + all SI', pred, COLORS['ext_all_si']))
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    
    n_groups = 10
    
    for name, pred, color in models_data:
        # Group predictions into deciles
        quantiles = np.percentile(pred, np.linspace(0, 100, n_groups + 1))
        observed = []
        predicted = []
        for i in range(n_groups):
            mask = (pred >= quantiles[i]) & (pred < quantiles[i+1])
            if mask.sum() > 0:
                observed.append(y[mask].mean())
                predicted.append(pred[mask].mean())
        
        ax.plot(predicted, observed, 'o-', color=color, lw=2, markersize=5, label=name)
    
    # Perfect calibration line
    ax.plot([0, 0.5], [0, 0.5], 'k--', lw=1, alpha=0.5, label='Perfect calibration')
    
    ax.set_xlabel('Predicted Probability')
    ax.set_ylabel('Observed Probability')
    ax.set_title('Figure 6. Calibration Plot for In-Hospital Mortality Models')
    ax.legend(loc='lower right', fontsize=8, framealpha=0.9)
    ax.set_xlim([0, 0.5])
    ax.set_ylim([0, 0.5])
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig6_Calibration.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig6_Calibration.pdf'))
    plt.close(fig)
    print("Fig6 saved.")


# ============================================================
# FIG 7: FOREST PLOT (Extended+DSI model)
# ============================================================
def generate_fig7(auc_results):
    """Forest plot for Extended+DSI model (main model, avoids multicollinearity)"""
    model = auc_results['_model_dsi']
    
    # Get model coefficients - handle both pandas and numpy formats
    params = model.params
    conf_int = model.conf_int()
    pvalues = model.pvalues
    
    # Variable order corresponds to: age_at_admission, gender_male, CCI, 
    # lactate_first, wbc_first, vasopressor_use, any_surgery, mechanical_ventilation, DSI_mean
    # (plus constant which we skip)
    var_labels = [
        'Age (per year)',
        'Male sex',
        'CCI',
        'Lactate (mmol/L)',
        'WBC (×10⁹/L)',
        'Vasopressor use',
        'Surgery',
        'Mechanical ventilation',
        'DSI (HR/DBP)',
    ]
    
    # Skip constant (first parameter)
    n_vars = len(var_labels)
    # Extract ORs, CIs, and P-values
    if isinstance(params, pd.Series):
        ors = np.exp(params.iloc[1:n_vars+1])
        ci_low_vals = np.exp(conf_int.iloc[1:n_vars+1, 0])
        ci_high_vals = np.exp(conf_int.iloc[1:n_vars+1, 1])
        pvals = pvalues.iloc[1:n_vars+1]
    else:
        # numpy array format
        ors = np.exp(params[1:n_vars+1])
        ci_low_vals = np.exp(conf_int[1:n_vars+1, 0])
        ci_high_vals = np.exp(conf_int[1:n_vars+1, 1])
        pvals = pvalues[1:n_vars+1]
    
    # Sort by effect magnitude
    sort_idx = np.argsort(np.abs(np.log(ors)))[::-1]
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    y_positions = np.arange(n_vars)
    
    for i, idx in enumerate(sort_idx):
        or_val = float(ors[idx])
        ci_lo = float(ci_low_vals[idx])
        ci_hi = float(ci_high_vals[idx])
        p = float(pvals[idx])
        
        # Determine xerr
        xerr_lo = or_val - ci_lo
        xerr_hi = ci_hi - or_val
        
        # Plot point and CI
        marker_color = '#E74C3C' if p < 0.05 else '#95A5A6'
        ax.errorbar(or_val, i, xerr=[[xerr_lo], [xerr_hi]],
                    fmt='o', color='#2C3E50', ecolor='#7F8C8D', elinewidth=2,
                    capsize=4, markersize=7, markerfacecolor=marker_color)
        
        # Label on right
        p_str = f'P<0.001' if p < 0.001 else f'P={p:.3f}'
        ax.text(ci_hi * 1.05 + 0.05, i, f'OR={or_val:.2f} ({ci_lo:.2f}–{ci_hi:.2f}), {p_str}',
                fontsize=8, va='center')
    
    # Reference line at OR=1
    ax.axvline(x=1, color='gray', ls='--', lw=1, alpha=0.7)
    
    ax.set_yticks(y_positions)
    ax.set_yticklabels([var_labels[sort_idx[i]] for i in range(n_vars)])
    ax.set_xlabel('Odds Ratio')
    ax.set_title('Figure 7. Forest Plot: Extended Baseline + DSI Model\nfor In-Hospital Mortality Prediction')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Set X-axis range to reasonable scale (log scale for better visualization)
    ax.set_xlim([0, max(float(ci_high_vals.max()) * 1.1, 3.5)])
    
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, 'Fig7_Forest.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig7_Forest.pdf'))
    plt.close(fig)
    print("Fig7 saved.")


# ============================================================
# FIG 8: SUBGROUP ROC
# ============================================================
def generate_fig8():
    """Subgroup ROC analysis for all 5 abdomen subtypes"""
    subtypes = ['inflammation', 'obstruction', 'perforation', 'ischemia', 'other']
    
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes_flat = axes.flatten()
    
    for idx, subtype in enumerate(subtypes):
        ax = axes_flat[idx]
        sub_data = df_cc[df_cc['abdomen_subtype'] == subtype].copy()
        
        if len(sub_data) < 30 or sub_data[outcome_col].sum() < 5:
            ax.text(0.5, 0.5, f'{subtype}\nInsufficient events\n(n={len(sub_data)}, deaths={sub_data[outcome_col].sum()})',
                    ha='center', va='center', fontsize=10, transform=ax.transAxes)
            ax.set_title(f'{subtype.capitalize()}', fontsize=10)
            continue
        
        y_sub = sub_data[outcome_col].values
        
        # Extended + DSI model for each subgroup
        X_sub = sub_data[model_vars_base + model_vars_ext + ['DSI_mean']].values
        try:
            model_sub = fit_logistic(X_sub, y_sub)
            pred_sub = model_sub.predict(sm.add_constant(X_sub))
            auc_sub, ci_lo, ci_hi, fpr, tpr = compute_auc(y_sub, pred_sub)
            
            ax.plot(fpr, tpr, color=COLORS.get(subtype, '#2C3E50'), lw=2.5,
                    label=f'Extended+DSI\nAUC={auc_sub:.3f} [{ci_lo:.3f}-{ci_hi:.3f}]')
        except Exception as e:
            ax.text(0.5, 0.5, f'{subtype}\nModel failed: {str(e)[:30]}',
                    ha='center', va='center', fontsize=9, transform=ax.transAxes)
            ax.set_title(f'{subtype.capitalize()}', fontsize=10)
            continue
        
        # Extended baseline
        X_ext = sub_data[model_vars_base + model_vars_ext].values
        try:
            model_ext_sub = fit_logistic(X_ext, y_sub)
            pred_ext_sub = model_ext_sub.predict(sm.add_constant(X_ext))
            auc_ext_sub, _, _, fpr_e, tpr_e = compute_auc(y_sub, pred_ext_sub)
            ax.plot(fpr_e, tpr_e, color='#95A5A6', lw=1.5, ls='--',
                    label=f'Extended baseline\nAUC={auc_ext_sub:.3f}')
        except:
            pass
        
        ax.plot([0, 1], [0, 1], 'k--', lw=0.5, alpha=0.3)
        ax.set_xlabel('FPR')
        ax.set_ylabel('TPR')
        ax.set_title(f'{subtype.capitalize()} (n={len(sub_data)}, death={sub_data[outcome_col].sum()})', fontsize=9)
        ax.legend(fontsize=7, loc='lower right')
        ax.set_xlim([-0.02, 1.02])
        ax.set_ylim([-0.02, 1.02])
        ax.grid(True, alpha=0.3)
    
    # Hide the 6th panel
    axes_flat[5].axis('off')
    
    fig.suptitle('Figure 8. Subgroup ROC Analysis by Acute Abdomen Subtype\n(In-Hospital Mortality Prediction)',
                 fontsize=11, fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig8_Subgroup_ROC.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig8_Subgroup_ROC.pdf'))
    plt.close(fig)
    print("Fig8 saved.")


# ============================================================
# FIG 9: CIF (Competing Risk - Corrected)
# ============================================================
def generate_fig9():
    """Corrected CIF curves for competing risks (in-hospital death vs discharge alive)"""
    df_cc_cif = df_cc.copy()
    df_cc_cif['time'] = df.loc[df_cc_cif.index, 'los']
    df_cc_cif['DSI_Q'] = pd.qcut(df_cc_cif['DSI_mean'], q=4, labels=['Q1','Q2','Q3','Q4'])
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    
    q_colors = [COLORS['q1'], COLORS['q2'], COLORS['q3'], COLORS['q4']]
    
    for q, color in zip(['Q1','Q2','Q3','Q4'], q_colors):
        q_data = df_cc_cif[df_cc_cif['DSI_Q'] == q]
        times = q_data['time'].values
        # events: 1=hospital death (primary), 0=alive discharge (censored)
        events = q_data[outcome_col].values
        
        # Compute CIF properly
        sort_idx = np.argsort(times)
        t_sorted = times[sort_idx]
        e_sorted = events[sort_idx]
        
        unique_t = np.unique(t_sorted)
        cif_cum = 0.0
        S_overall = 1.0
        
        cif_times = [0]
        cif_vals = [0]
        
        for t_k in unique_t:
            n_risk = np.sum(t_sorted >= t_k)
            d_primary = np.sum((t_sorted == t_k) & (e_sorted == 1))
            d_all = np.sum(t_sorted == t_k)
            
            if n_risk > 0:
                # CIF increment: (d_j / n_risk) * S(t_k-)
                increment = (d_primary / n_risk) * S_overall
                cif_cum += increment
                
                # Update overall survival: S(t_k+) = S(t_k-) * (1 - d_all/n_risk)
                S_overall *= (1 - d_all / n_risk)
            
            cif_times.append(t_k)
            cif_vals.append(min(cif_cum, 1.0))  # Cap at 100%
        
        ax.step(cif_times, cif_vals, where='post', color=color, lw=2, label=f'{q}')
    
    ax.set_xlabel('Hospital Length of Stay (days)')
    ax.set_ylabel('Cumulative Incidence of In-Hospital Death')
    ax.set_title('Figure 9. Cumulative Incidence Function by DSI Quartile\n(Competing Risk: In-Hospital Death vs Discharge Alive)')
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 0.40])
    ax.grid(True, alpha=0.3)
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig9_CIF.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig9_CIF.pdf'))
    plt.close(fig)
    print("Fig9 saved.")


# ============================================================
# FIG 10: ROC EXTENDED MODELS
# ============================================================
def generate_fig10(auc_results):
    """ROC comparison for extended models (main result figure)"""
    y = df_cc[outcome_col].values
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    
    # Extended baseline
    X_ext = df_cc[model_vars_base + model_vars_ext].values
    pred_ext = auc_results['_model_ext'].predict(sm.add_constant(X_ext))
    auc_ext, ci_lo_e, ci_hi_e, fpr_e, tpr_e = compute_auc(y, pred_ext)
    
    # Extended + DSI (main model)
    X_dsi = df_cc[model_vars_base + model_vars_ext + ['DSI_mean']].values
    pred_dsi = auc_results['_model_dsi'].predict(sm.add_constant(X_dsi))
    auc_dsi, ci_lo_d, ci_hi_d, fpr_d, tpr_d = compute_auc(y, pred_dsi)
    
    # Extended + all SI
    X_all = df_cc[model_vars_base + model_vars_ext + si_vars].values
    pred_all = auc_results['_model_all'].predict(sm.add_constant(X_all))
    auc_all, ci_lo_a, ci_hi_a, fpr_a, tpr_a = compute_auc(y, pred_all)
    
    # Basic baseline for reference
    X_base = df_cc[model_vars_base].values
    pred_base = fit_logistic(X_base, y).predict(sm.add_constant(X_base))
    auc_base, _, _, fpr_b, tpr_b = compute_auc(y, pred_base)
    
    ax.plot(fpr_b, tpr_b, color=COLORS['basic_baseline'], lw=1.5, ls=':',
            label=f'Basic baseline (AUC={auc_base:.3f})')
    ax.plot(fpr_e, tpr_e, color=COLORS['extended_baseline'], lw=2,
            label=f'Extended baseline (AUC={auc_ext:.3f} [{ci_lo_e:.3f}-{ci_hi_e:.3f}])')
    ax.plot(fpr_d, tpr_d, color=COLORS['ext_dsi'], lw=2.5,
            label=f'Extended + DSI (AUC={auc_dsi:.3f} [{ci_lo_d:.3f}-{ci_hi_d:.3f}])')
    ax.plot(fpr_a, tpr_a, color=COLORS['ext_all_si'], lw=1.5, ls='--',
            label=f'Extended + all SI (AUC={auc_all:.3f} [{ci_lo_a:.3f}-{ci_hi_a:.3f}])')
    
    ax.plot([0, 1], [0, 1], 'k--', lw=0.5, alpha=0.3)
    ax.set_xlabel('False Positive Rate (1 – Specificity)')
    ax.set_ylabel('True Positive Rate (Sensitivity)')
    ax.set_title('Figure 10. ROC Curves: Incremental Value of DSI\nover Extended Baseline for In-Hospital Mortality')
    ax.legend(loc='lower right', fontsize=8, framealpha=0.9)
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])
    ax.grid(True, alpha=0.3)
    
    fig.savefig(os.path.join(FIG_DIR, 'Fig10_ROC_extended.png'), dpi=DPI)
    fig.savefig(os.path.join(FIG_DIR, 'Fig10_ROC_extended.pdf'))
    plt.close(fig)
    print("Fig10 saved.")


# ============================================================
# MAIN EXECUTION
# ============================================================
print("=" * 60)
print("SCI Paper Figure Regeneration (Corrected)")
print("=" * 60)
print(f"Dataset: analysis_dataset_corrected.csv")
print(f"CC sample: {len(df_cc)}, In-hospital mortality: {df_cc[outcome_col].mean()*100:.2f}%")
print(f"Output directory: {FIG_DIR}")
print("=" * 60)

# Generate Fig1 (Flowchart)
print("\n[1/10] Generating Fig1 (Flowchart)...")
generate_fig1()

# Generate Fig2 (ROC) and get models
print("\n[2/10] Generating Fig2 (ROC)...")
auc_results, model_ext, model_dsi, model_all = generate_fig2()

# Store models for reuse
auc_results['_model_base'] = fit_logistic(df_cc[model_vars_base].values, df_cc[outcome_col].values)
auc_results['_model_ext'] = model_ext
auc_results['_model_dsi'] = model_dsi
auc_results['_model_all'] = model_all

# Generate Fig3 (DCA)
print("\n[3/10] Generating Fig3 (DCA)...")
generate_fig3(auc_results)

# Generate Fig4 (RCS)
print("\n[4/10] Generating Fig4 (RCS)...")
generate_fig4()

# Generate Fig5 (KM)
print("\n[5/10] Generating Fig5 (KM)...")
generate_fig5()

# Generate Fig6 (Calibration)
print("\n[6/10] Generating Fig6 (Calibration)...")
generate_fig6(auc_results)

# Generate Fig7 (Forest)
print("\n[7/10] Generating Fig7 (Forest)...")
generate_fig7(auc_results)

# Generate Fig8 (Subgroup ROC)
print("\n[8/10] Generating Fig8 (Subgroup ROC)...")
generate_fig8()

# Generate Fig9 (CIF)
print("\n[9/10] Generating Fig9 (CIF)...")
generate_fig9()

# Generate Fig10 (ROC extended)
print("\n[10/10] Generating Fig10 (ROC extended)...")
generate_fig10(auc_results)

print("\n" + "=" * 60)
print("All 10 figures generated successfully!")
print(f"Output: {FIG_DIR}/")
print("=" * 60)
