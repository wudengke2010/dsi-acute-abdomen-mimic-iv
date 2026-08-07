"""
Generate component decomposition supplementary figure (Fig S8)
Following Ospina-Tascón 2020 Figure 2/3 style:
- Panel A: AUC bar chart for individual components vs DSI
- Panel B: DBP-matched mortality by DSI tertile (heatmap-style)
- Panel C: HR-matched mortality by DSI tertile
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.metrics import roc_auc_score

BASE = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'
OUT = f'{BASE}/figures_v7'

df = pd.read_csv(f'{BASE}/analysis_dataset_revised.csv')
y = df['hospital_expire_flag'].values

# Compute AUCs
components = {
    'HR': df['HR_mean'].values,
    'DBP': df['DBP_mean'].values,
    'SBP': df['SBP_mean'].values,
    'MAP': df['MAP_mean'].values,
    'SI': df['SI_mean'].values,
    'MSI': df['MSI_mean'].values,
    'DSI': df['DSI_mean'].values,
    'Age-SI': df['Age_SI_mean'].values,
    'Lactate': df['lactate_first'].values,
    'SOFA': df['sofa'].values,
}

aucs = {}
for name, vals in components.items():
    v = pd.Series(vals).dropna()
    yv = y[v.index]
    auc = roc_auc_score(yv, v)
    if name in ['DBP', 'SBP', 'MAP']:
        auc = 1 - auc
    aucs[name] = auc

# Create figure
fig = plt.figure(figsize=(14, 5))
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1.2, 1.2], wspace=0.35)

# Panel A: AUC bar chart
ax1 = fig.add_subplot(gs[0])
names = ['HR', 'DBP', 'SBP', 'MAP', 'SI', 'MSI', 'DSI', 'Age-SI', 'Lactate', 'SOFA']
auc_vals = [aucs[n] for n in names]
colors = ['#C0C0C0'] * 4 + ['#A8D8A8'] * 4 + ['#FFB347', '#FF6B6B']  # BP gray, SI derivatives green, Lactate orange, SOFA red
bars = ax1.barh(range(len(names)), auc_vals, color=colors, edgecolor='black', linewidth=0.5)
ax1.set_yticks(range(len(names)))
ax1.set_yticklabels(names, fontsize=9)
ax1.set_xlabel('AUC for In-Hospital Mortality', fontsize=10)
ax1.set_xlim(0.5, 0.8)
ax1.axvline(x=0.5, color='gray', linestyle='--', linewidth=0.5)
ax1.set_title('A: Individual Predictor Performance', fontsize=11, fontweight='bold')
for i, v in enumerate(auc_vals):
    ax1.text(v + 0.005, i, f'{v:.3f}', va='center', fontsize=8)
# Highlight DSI bar
bars[6].set_edgecolor('darkgreen')
bars[6].set_linewidth(2)

# Panel B: DBP-matched mortality by DSI tertile
ax2 = fig.add_subplot(gs[1])
df['dbp_q'] = pd.qcut(df['DBP_mean'], 5, labels=['Q1\n(low)', 'Q2', 'Q3', 'Q4', 'Q5\n(high)'])
df['dsi_t'] = pd.qcut(df['DSI_mean'], 3, labels=['Low DSI', 'Mid DSI', 'High DSI'])

dbp_labels = ['Q1\n(low)', 'Q2', 'Q3', 'Q4', 'Q5\n(high)']
dsi_labels = ['Low DSI', 'Mid DSI', 'High DSI']
mortality_matrix_b = np.zeros((5, 3))
for i, dbp_q in enumerate(dbp_labels):
    for j, dsi_t in enumerate(dsi_labels):
        subset = df[(df['dbp_q'] == dbp_q) & (df['dsi_t'] == dsi_t)]
        if len(subset) > 0:
            mortality_matrix_b[i, j] = subset['hospital_expire_flag'].mean() * 100

im = ax2.imshow(mortality_matrix_b, cmap='YlOrRd', aspect='auto', vmin=10, vmax=35)
ax2.set_xticks(range(3))
ax2.set_xticklabels(dsi_labels, fontsize=9)
ax2.set_yticks(range(5))
ax2.set_yticklabels(dbp_labels, fontsize=9)
ax2.set_xlabel('DSI Tertile', fontsize=10)
ax2.set_ylabel('DBP Quintile', fontsize=10)
ax2.set_title('B: Mortality (%) by DBP Quintile\nand DSI Tertile', fontsize=11, fontweight='bold')
for i in range(5):
    for j in range(3):
        val = mortality_matrix_b[i, j]
        n = len(df[(df['dbp_q'] == dbp_labels[i]) & (df['dsi_t'] == dsi_labels[j])])
        color = 'white' if val > 25 else 'black'
        ax2.text(j, i, f'{val:.1f}%\n(n={n})', ha='center', va='center', fontsize=7.5, color=color)
plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04, label='Mortality (%)')

# Panel C: HR-matched mortality by DSI tertile
ax3 = fig.add_subplot(gs[2])
df['hr_q'] = pd.qcut(df['HR_mean'], 5, labels=['Q1\n(low)', 'Q2', 'Q3', 'Q4', 'Q5\n(high)'])

hr_labels = ['Q1\n(low)', 'Q2', 'Q3', 'Q4', 'Q5\n(high)']
mortality_matrix_c = np.zeros((5, 3))
for i, hr_q in enumerate(hr_labels):
    for j, dsi_t in enumerate(dsi_labels):
        subset = df[(df['hr_q'] == hr_q) & (df['dsi_t'] == dsi_t)]
        if len(subset) > 0:
            mortality_matrix_c[i, j] = subset['hospital_expire_flag'].mean() * 100

im2 = ax3.imshow(mortality_matrix_c, cmap='YlOrRd', aspect='auto', vmin=8, vmax=36)
ax3.set_xticks(range(3))
ax3.set_xticklabels(dsi_labels, fontsize=9)
ax3.set_yticks(range(5))
ax3.set_yticklabels(hr_labels, fontsize=9)
ax3.set_xlabel('DSI Tertile', fontsize=10)
ax3.set_ylabel('HR Quintile', fontsize=10)
ax3.set_title('C: Mortality (%) by HR Quintile\nand DSI Tertile', fontsize=11, fontweight='bold')
for i in range(5):
    for j in range(3):
        val = mortality_matrix_c[i, j]
        n = len(df[(df['hr_q'] == hr_labels[i]) & (df['dsi_t'] == dsi_labels[j])])
        color = 'white' if val > 25 else 'black'
        ax3.text(j, i, f'{val:.1f}%\n(n={n})', ha='center', va='center', fontsize=7.5, color=color)
plt.colorbar(im2, ax=ax3, fraction=0.046, pad=0.04, label='Mortality (%)')

plt.tight_layout()
plt.savefig(f'{OUT}/FigS8_Component_Decomposition.png', dpi=300, bbox_inches='tight')
plt.savefig(f'{OUT}/FigS8_Component_Decomposition.pdf', bbox_inches='tight')
plt.close()
print(f"Figure saved: {OUT}/FigS8_Component_Decomposition.png + .pdf")
