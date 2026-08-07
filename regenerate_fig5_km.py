"""
Standalone regeneration of Fig5_KM.png with legend moved to upper-right.
Avoids PDF/SVG fontTools DLL issues by saving PNG only.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
import warnings
warnings.filterwarnings('ignore')

# Constants from generate_figures_publication.py
DPI = 300
FIG_DIR = 'figures_publication'
os.makedirs(FIG_DIR, exist_ok=True)

C = {
    'q1': '#0072B2',
    'q2': '#009E73',
    'q3': '#E69F00',
    'q4': '#D55E00',
}

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 8,
    'axes.titlesize': 9,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'figure.dpi': DPI,
    'savefig.dpi': DPI,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'grid.linewidth': 0.4,
    'lines.linewidth': 1.4,
    'mathtext.default': 'regular',
})

W_SINGLE = 3.54

def fmt_p(p):
    if p < 0.001:
        return 'P < 0.001'
    elif p < 0.01:
        return f'P = {p:.3f}'
    else:
        return f'P = {p:.2f}'

# Load data (use revised CC dataset to match current manuscript N=5,728)
df = pd.read_csv('analysis_dataset_revised.csv')
outcome_col = 'hospital_expire_flag'
df_cc = df.copy()

# FIG 5: KAPLAN-MEIER (with number-at-risk)
from lifelines.statistics import multivariate_logrank_test

df_km = df_cc.copy()
df_km['time'] = df_km['los']
df_km['event'] = df_km[outcome_col]
df_km['DSI_Q'] = pd.qcut(df_km['DSI_mean'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

fig = plt.figure(figsize=(W_SINGLE, W_SINGLE * 1.15))
gs = GridSpec(2, 1, figure=fig, height_ratios=[4, 1.1], hspace=0.22,
              left=0.14, right=0.96, top=0.92, bottom=0.08)
ax = fig.add_subplot(gs[0])
risk_ax = fig.add_subplot(gs[1])

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

    ax.step(s_times, survival, where='post', color=color, lw=1.6, label=label)
    km_data[q] = (times_s, events_s)

result = multivariate_logrank_test(df_km['time'], df_km['DSI_Q'], df_km['event'])
p_val = result.p_value
ax.text(0.97, 0.97, f'Log-rank {fmt_p(p_val)}', transform=ax.transAxes,
        fontsize=7, va='top', ha='right',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.95,
                  edgecolor='#CCCCCC', linewidth=0.5))

ax.set_xlabel('')
ax.set_ylabel('In-Hospital Survival Probability')

# IMPORTANT: Legend placed in upper-right empty region to avoid blocking survival curves.
ax.legend(loc='upper right', bbox_to_anchor=(0.98, 0.85), framealpha=0.95,
          edgecolor='#CCCCCC', fontsize=7)

ax.set_xlim([0, max_t])
ax.set_ylim([0.55, 1.02])
ax.grid(True, alpha=0.15, linewidth=0.3)

# Number at risk table in dedicated subplot
risk_ax.set_xlim(0, max_t)
risk_ax.set_ylim(-0.5, 4.5)
risk_ax.axis('off')
risk_ax.text(-1.5, 3.5, 'No. at risk', fontsize=6.5, ha='right', va='center')

for i, (q, color) in enumerate(zip(['Q1', 'Q2', 'Q3', 'Q4'], q_colors)):
    times_s, events_s = km_data[q]
    row_y = 3 - i - 0.5
    risk_ax.text(-1.5, row_y, q, fontsize=6.5, ha='right', va='center', color=color)
    for tp in time_points:
        n_risk = np.sum(times_s > tp)
        risk_ax.text(tp, row_y, str(n_risk), fontsize=6.5, ha='center', va='center')

for tp in time_points:
    risk_ax.text(tp, 3.5, str(tp), fontsize=6.5, ha='center', va='bottom')

risk_ax.set_xlabel('Hospital Length of Stay (days)', fontsize=8)
risk_ax.xaxis.set_label_coords(0.5, -0.15)

fig.savefig(os.path.join(FIG_DIR, 'Fig5_KM.png'), dpi=DPI, bbox_inches='tight', pad_inches=0.05)
print(f'  Fig5_KM.png saved to {FIG_DIR}/')
plt.close(fig)
