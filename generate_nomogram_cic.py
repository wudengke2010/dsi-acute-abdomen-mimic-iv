"""
Generate improved Nomogram and Clinical Impact Curve (CIC) for v8 paper.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import os

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0

OUT_DIR = 'figures_v7'
os.makedirs(OUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv('analysis_dataset_revised.csv')
df['gender_num'] = (df['gender'] == 'M').astype(int)

# Primary model (no surgery)
cols_full = ['age_at_admission','gender_num','CCI','lactate_first','wbc_first',
             'vasopressor_use','mechanical_ventilation','sofa','DSI_mean']
X_full = df[cols_full].values.astype(float)
y = df['hospital_expire_flag'].values.astype(float)

lr_full = LogisticRegression(max_iter=5000, C=1e10, solver='lbfgs')
lr_full.fit(X_full, y)

# Simplified model
cols_simple = ['age_at_admission','lactate_first','sofa','DSI_mean']
X_simple = df[cols_simple].values.astype(float)
lr_simple = LogisticRegression(max_iter=5000, C=1e10, solver='lbfgs')
lr_simple.fit(X_simple, y)

print(f'Full model AUC: {roc_auc_score(y, lr_full.predict_proba(X_full)[:,1]):.4f}')
print(f'Simple model AUC: {roc_auc_score(y, lr_simple.predict_proba(X_simple)[:,1]):.4f}')


def draw_nomogram_axes(ax, model, var_info, title, max_total=200):
    """Draw a clean nomogram on given axes."""
    intercept = model.intercept_[0]
    betas = model.coef_[0]
    
    ax.set_xlim(-0.10, 1.05)
    ax.set_ylim(-0.18, 1.05)
    
    # Points axis (left side)
    ax.text(-0.065, 0.95, 'Points', ha='center', va='bottom', fontsize=10, fontweight='bold', rotation=90)
    for pt in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        y = 0.92 - pt / 100.0 * 0.82
        ax.plot([-0.04, -0.01], [y, y], 'k-', lw=0.8)
        ax.text(-0.05, y, str(pt), ha='right', va='center', fontsize=8)
    
    # Calculate max contribution for normalization
    max_contrib = max(abs(betas[i] * (var_info[i][3] - var_info[i][2])) for i in range(len(var_info)))
    baseline_lp = intercept + sum(betas[i] * var_info[i][2] for i in range(len(var_info)))
    
    n_vars = len(var_info)
    y_positions = np.linspace(0.82, 0.15, n_vars)
    row_height = 0.06
    x_start = 0.10
    x_end = 0.95
    
    for i, (name, col, vmin, vmax, vstep, decimals) in enumerate(var_info):
        beta = betas[i]
        y_base = y_positions[i]
        contrib_min = beta * vmin
        contrib_max = beta * vmax
        contrib_range = contrib_max - contrib_min
        
        # Variable name - wrap long labels
        if len(name) > 18:
            parts = name.split('(')
            label_text = parts[0] + '\n(' + '('.join(parts[1:])
        else:
            label_text = name
        ax.text(-0.005, y_base, label_text, ha='right', va='center', fontsize=8.5, fontweight='bold')
        
        # Scale line
        ax.plot([x_start, x_end], [y_base, y_base], 'k-', lw=1.2)
        
        # Special labels
        if col == 'gender_num':
            for val, label in [(0, 'Female'), (1, 'Male')]:
                points = abs((beta * val - contrib_min) / max_contrib) * 100
                x_pos = x_start + (points / 100.0) * (x_end - x_start)
                ax.plot([x_pos, x_pos], [y_base - 0.015, y_base + 0.015], 'k-', lw=1)
                ax.text(x_pos, y_base - 0.038, label, ha='center', va='top', fontsize=8)
        elif col in ['vasopressor_use', 'mechanical_ventilation']:
            for val, label in [(0, 'No'), (1, 'Yes')]:
                points = abs((beta * val - contrib_min) / max_contrib) * 100
                x_pos = x_start + (points / 100.0) * (x_end - x_start)
                ax.plot([x_pos, x_pos], [y_base - 0.015, y_base + 0.015], 'k-', lw=1)
                ax.text(x_pos, y_base - 0.038, label, ha='center', va='top', fontsize=8)
        else:
            vals = np.arange(vmin, vmax + vstep/2, vstep)
            for val in vals:
                if col == 'wbc_first' and val > 0 and val % 10 != 0:
                    continue  # show only 0,10,20,30 for WBC
                points = abs((beta * val - contrib_min) / max_contrib) * 100
                x_pos = x_start + (points / 100.0) * (x_end - x_start)
                if x_pos > x_end:
                    x_pos = x_end
                ax.plot([x_pos, x_pos], [y_base - 0.015, y_base + 0.015], 'k-', lw=0.7)
                fmt = f'{val:.{decimals}f}'
                ax.text(x_pos, y_base - 0.038, fmt, ha='center', va='top', fontsize=7.5,
                       rotation=0)
    
    # Total Points axis
    y_total = 0.05
    ax.text(-0.005, y_total, 'Total\nPoints', ha='right', va='center', fontsize=9, fontweight='bold')
    ax.plot([x_start, x_end], [y_total, y_total], 'k-', lw=1.2)
    total_ticks = [0, 25, 50, 75, 100, 125, 150, 175, 200]
    for pt in total_ticks:
        x_pos = x_start + (pt / max_total) * (x_end - x_start)
        if x_pos <= x_end:
            ax.plot([x_pos, x_pos], [y_total - 0.015, y_total + 0.015], 'k-', lw=0.7)
            ax.text(x_pos, y_total - 0.038, str(pt), ha='center', va='top', fontsize=7.5)
    
    # Risk axis
    y_risk = -0.05
    ax.text(-0.005, y_risk, 'Risk of\nDeath', ha='right', va='center', fontsize=9, fontweight='bold')
    ax.plot([x_start, x_end], [y_risk, y_risk], 'k-', lw=1.2)
    
    for risk in [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60]:
        lp = np.log(risk / (1 - risk))
        total_pts = (lp - baseline_lp) / max_contrib * 100
        x_pos = x_start + (total_pts / max_total) * (x_end - x_start)
        if x_start <= x_pos <= x_end:
            ax.plot([x_pos, x_pos], [y_risk - 0.015, y_risk + 0.015], 'k-', lw=0.7)
            ax.text(x_pos, y_risk - 0.038, f'{risk:.0%}', ha='center', va='top', fontsize=7.5)
    
    ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    ax.axis('off')


# Generate FIGURE S9: Full + Simple Nomogram
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

var_info_full = [
    ('Age (yr)', 'age_at_admission', 18, 95, 10, 0),
    ('Gender', 'gender_num', 0, 1, 1, 0),
    ('CCI', 'CCI', 0, 10, 1, 0),
    ('Lactate (mmol/L)', 'lactate_first', 0.5, 10, 1, 1),
    ('WBC (×10⁹/L)', 'wbc_first', 0, 30, 10, 0),
    ('Vasopressor', 'vasopressor_use', 0, 1, 1, 0),
    ('MV', 'mechanical_ventilation', 0, 1, 1, 0),
    ('SOFA', 'sofa', 0, 24, 2, 0),
    ('DSI', 'DSI_mean', 0.5, 3.5, 0.5, 1),
]
draw_nomogram_axes(ax1, lr_full, var_info_full, 'A. Full Model\n(Age + CCI + Lactate + WBC + Vasopressor + MV + SOFA + DSI)')

var_info_simple = [
    ('Age (yr)', 'age_at_admission', 18, 95, 10, 0),
    ('Lactate (mmol/L)', 'lactate_first', 0.5, 10, 1, 1),
    ('SOFA', 'sofa', 0, 24, 2, 0),
    ('DSI', 'DSI_mean', 0.5, 3.5, 0.5, 1),
]
draw_nomogram_axes(ax2, lr_simple, var_info_simple, 'B. Rapid Bedside Model\n(Age + Lactate + SOFA + DSI)')

fig.suptitle('Nomograms for Predicting In-hospital Mortality in Acute Abdomen', 
             fontsize=13, fontweight='bold', y=1.00)

plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'FigS9_Nomogram.png'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(OUT_DIR, 'FigS9_Nomogram.pdf'), dpi=300, bbox_inches='tight')
plt.close()
print('FigS9_Nomogram (full + simple) generated successfully')


# Generate FIGURE S10: CIC
probs_full = lr_full.predict_proba(X_full)[:, 1]
probs_base = LogisticRegression(max_iter=5000, C=1e10, solver='lbfgs').fit(
    df[['age_at_admission','gender_num','CCI','lactate_first','wbc_first',
        'vasopressor_use','mechanical_ventilation','sofa']].values.astype(float), y
).predict_proba(
    df[['age_at_admission','gender_num','CCI','lactate_first','wbc_first',
        'vasopressor_use','mechanical_ventilation','sofa']].values.astype(float)
)[:, 1]

threshold_prob = np.arange(0.05, 0.95, 0.01)
n_total = len(y)

high_risk_full, true_pos_full, false_pos_full = [], [], []
high_risk_base, true_pos_base = [], []

for t in threshold_prob:
    c_full = probs_full >= t
    high_risk_full.append(np.sum(c_full) / n_total * 100)
    true_pos_full.append(np.sum(c_full & (y == 1)) / n_total * 100)
    false_pos_full.append(np.sum(c_full & (y == 0)) / n_total * 100)
    
    c_base = probs_base >= t
    high_risk_base.append(np.sum(c_base) / n_total * 100)
    true_pos_base.append(np.sum(c_base & (y == 1)) / n_total * 100)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

for ax, hr, tp, fp, label in [(ax1, high_risk_full, true_pos_full, false_pos_full, '+ DSI'),
                               (ax2, high_risk_base, true_pos_base, None, '(No DSI)')]:
    ax.plot(threshold_prob, hr, 'r-', lw=2.2, label='High-risk classified (per 100)')
    ax.plot(threshold_prob, tp, 'b-', lw=2.2, label='True positives (per 100)')
    if fp is not None:
        ax.plot(threshold_prob, fp, color='orange', ls='--', lw=1.5, label='False positives (per 100)')
    ax.fill_between(threshold_prob, tp, hr, alpha=0.12, color='red')
    ax.set_xlabel('Risk Threshold', fontsize=11)
    ax.set_ylabel('Number per 100 Patients', fontsize=11)
    ax.set_title(f'{label}', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    ax.set_xlim(0.05, 0.95)
    ax.set_ylim(0, 60)
    ax.tick_params(direction='in')
    ax.grid(False)
    
    idx = np.argmin(np.abs(threshold_prob - 0.10))
    fp_text = f'\n{fp[idx]:.1f} false pos' if fp is not None else ''
    ax.annotate(f'At 10% threshold:\n{hr[idx]:.1f} high-risk\n{tp[idx]:.1f} true pos{fp_text}',
               xy=(0.10, hr[idx]), xytext=(0.20, 45),
               fontsize=8, arrowprops=dict(arrowstyle='->', color='gray', lw=0.8),
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF5E6', edgecolor='orange', alpha=0.9))

fig.suptitle('Clinical Impact Curves: High-Risk Classified and True Positive Patients per 100',
            fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'FigS10_CIC.png'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(OUT_DIR, 'FigS10_CIC.pdf'), dpi=300, bbox_inches='tight')
plt.close()
print('FigS10_CIC generated successfully')


# DSI threshold diagnostic performance
dsi = df['DSI_mean'].values
death = df['hospital_expire_flag'].values
thresholds = [1.0, 1.279, 1.502, 1.762, 2.0]
results = []
for t in thresholds:
    pred = dsi >= t
    tp = np.sum(pred & (death == 1)); fp = np.sum(pred & (death == 0))
    tn = np.sum(~pred & (death == 0)); fn = np.sum(~pred & (death == 1))
    se = tp / (tp + fn); sp = tn / (tn + fp)
    ppv = tp / (tp + fp); npv = tn / (tn + fn)
    results.append({'Threshold': t, 'TP': tp, 'FP': fp, 'TN': tn, 'FN': fn,
                   'Sensitivity': se, 'Specificity': sp, 'PPV': ppv, 'NPV': npv,
                   'Youden': se + sp - 1})
res_df = pd.DataFrame(results)
res_df.to_csv('DSI_diagnostic_performance.csv', index=False)
print('\n=== DSI Diagnostic Performance ===')
print(res_df[['Threshold','Sensitivity','Specificity','PPV','NPV','Youden']].to_string(index=False))
