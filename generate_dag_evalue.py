"""
Generate DAG figure (FigS11) and E-value analysis (Table S13) for P0 risk mitigation.
"""
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, 'figures_v7')
os.makedirs(OUTDIR, exist_ok=True)

# Node positions: key -> (x, y)
node_pos = {
    'Age':           (1.0, 7.5),
    'Sex':           (1.0, 5.5),
    'CCI':           (1.0, 3.5),
    'Severity':      (1.0, 1.5),
    'DSI':           (4.5, 7.0),
    'Lactate':       (4.5, 5.5),
    'WBC':           (4.5, 4.0),
    'SOFA':          (4.5, 2.5),
    'Vasopressor':   (4.5, 1.0),
    'MV':            (7.0, 7.5),
    'Collider':      (7.5, 2.5),
    'Mortality':     (10.5, 5.0),
}

# Display labels
node_label = {
    'Age':       'Age',
    'Sex':       'Sex',
    'CCI':       'Comorbidity\n(CCI)',
    'Severity':  'Acute Abdomen\nSeverity',
    'DSI':       'DSI (HR/DBP)',
    'Lactate':   'Lactate',
    'WBC':       'WBC',
    'SOFA':      'SOFA',
    'Vasopressor':'Vasopressor',
    'MV':        'Mechanical\nVentilation',
    'Collider':  'Lactate/WBC\nMeasurement\n(Collider)',
    'Mortality': 'In-hospital\nMortality',
}

# Colors
C_CONF   = '#E8EAF6'   # confounders
C_EXPO   = '#FFF3E0'   # exposure
C_OUT    = '#FFEBEE'   # outcome
C_COLL   = '#FCE4EC'   # collider
C_INT    = '#E8F5E9'   # intermediates

node_color = {
    'Age': C_CONF, 'Sex': C_CONF, 'CCI': C_CONF,
    'Severity': C_INT,
    'DSI': C_EXPO,
    'Lactate': C_INT, 'WBC': C_INT, 'SOFA': C_INT,
    'Vasopressor': C_INT, 'MV': C_INT,
    'Collider': C_COLL,
    'Mortality': C_OUT,
}

node_border = {
    'DSI': '#E65100',
    'Mortality': '#C62828',
    'Collider': '#AD1457',
}

# Edges
edges = [
    ('Age', 'DSI'), ('Age', 'CCI'), ('Age', 'Mortality'),
    ('Sex', 'DSI'),
    ('CCI', 'DSI'), ('CCI', 'Mortality'),
    ('Severity', 'DSI'), ('Severity', 'Lactate'), ('Severity', 'WBC'),
    ('Severity', 'SOFA'), ('Severity', 'Vasopressor'), ('Severity', 'Mortality'),
    ('Severity', 'MV'),
    ('DSI', 'Mortality'),
    ('Lactate', 'Collider'), ('WBC', 'Collider'),
    ('Collider', 'Mortality'),
    ('Lactate', 'Mortality'), ('WBC', 'Mortality'),
    ('SOFA', 'Mortality'), ('Vasopressor', 'Mortality'),
    ('MV', 'Mortality'),
    ('SOFA', 'DSI'),
]

# ====== DRAW ======
fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')

for src, dst in edges:
    sx, sy = node_pos[src]
    dx, dy = node_pos[dst]
    
    if src == 'Collider':
        ec, lw, ls = '#C62828', 1.5, 'dashed'
    elif src == 'DSI' and dst == 'Mortality':
        ec, lw, ls = '#E65100', 2.5, 'solid'
    else:
        ec, lw, ls = '#546E7A', 1.0, 'solid'
    
    ax.annotate('', xy=(dx, dy), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color=ec, lw=lw,
                               linestyle=ls, connectionstyle='arc3,rad=0.05'))

# OR label on DSI->Mortality
mx = (node_pos['DSI'][0] + node_pos['Mortality'][0]) / 2
my = (node_pos['DSI'][1] + node_pos['Mortality'][1]) / 2
ax.text(mx + 0.15, my + 0.3, 'OR=2.18', fontsize=9, color='#E65100',
        fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF3E0',
                 edgecolor='#E65100', alpha=0.9))

# Collider annotation
cx = (node_pos['Collider'][0] + node_pos['Mortality'][0]) / 2
cy = (node_pos['Collider'][1] + node_pos['Mortality'][1]) / 2
ax.text(cx + 0.1, cy - 0.2, 'Conditioning\nopens backdoor', fontsize=7,
        color='#C62828', ha='center', style='italic')

# Draw nodes
for key, (x, y) in node_pos.items():
    label = node_label[key]
    lines = label.count('\n') + 1
    # Width based on longest line
    max_line = max(label.split('\n'), key=len)
    w = max(2.0, len(max_line) * 0.15 + 0.6)
    h = lines * 0.55 + 0.2
    
    if key == 'Collider':
        w = 2.5; h = 1.2
    elif key == 'Severity':
        w = 2.4; h = 0.85
    elif key == 'Mortality':
        w = 2.2; h = 0.85
    
    fill = node_color[key]
    edge = node_border.get(key, '#546E7A')
    lw = 2.5 if key in node_border else 1.5
    
    fancy = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle='round,pad=0.08', facecolor=fill,
                           edgecolor=edge, linewidth=lw, zorder=5)
    ax.add_patch(fancy)
    ax.text(x, y, label, ha='center', va='center', fontsize=9,
            fontweight='bold' if key in node_border else 'normal',
            color='#212121', zorder=6)

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_EXPO, edgecolor='#E65100', label='Exposure (DSI)'),
    mpatches.Patch(facecolor=C_OUT, edgecolor='#C62828', label='Outcome'),
    mpatches.Patch(facecolor=C_INT, edgecolor='#546E7A', label='Measured covariates'),
    mpatches.Patch(facecolor=C_CONF, edgecolor='#546E7A', label='Demographics'),
    mpatches.Patch(facecolor=C_COLL, edgecolor='#AD1457', label='Collider (bias)'),
]
ax.legend(handles=legend_elements, loc='lower left', framealpha=0.9,
          fontsize=8, ncol=3, bbox_to_anchor=(0.02, 0.02))

ax.text(6.0, 8.7, 'Figure S11. Directed Acyclic Graph (DAG) for DSI and In-Hospital Mortality',
        fontsize=11, fontweight='bold', ha='center')
ax.text(6.0, 8.35, 'Conditioning on lactate/WBC measurement (complete-case) opens collider pathway, biasing DSI-mortality association.',
        fontsize=8, ha='center', style='italic', color='#616161')

for fmt in ['png', 'pdf']:
    path = os.path.join(OUTDIR, f'FigS11_DAG.{fmt}')
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f'Saved: {path}')
plt.close()

# ====== E-VALUE ======
or_point = 2.18
or_lower = 1.79
or_upper = 2.65

def e_val(rr):
    if rr <= 1:
        return float('nan')
    return rr + math.sqrt(rr * (rr - 1))

ep = e_val(or_point)
el = e_val(or_lower)

print(f"\n=== E-value Analysis ===")
print(f"Point OR={or_point} -> E={ep:.2f}")
print(f"CI lower OR={or_lower} -> E={el:.2f}")

import csv
csv_path = os.path.join(BASE, 'Table_S13_Evalue.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Parameter', 'Value', 'E-value', 'Interpretation'])
    w.writerow(['DSI OR (point estimate)', f'{or_point:.2f}', f'{ep:.2f}',
                f'Unmeasured confounder RR>={ep:.1f} needed to nullify'])
    w.writerow(['DSI OR (CI lower bound)', f'{or_lower:.2f}', f'{el:.2f}',
                f'Unmeasured confounder RR>={el:.1f} needed to shift CI to null'])
    w.writerow(['DSI OR (CI upper bound)', f'{or_upper:.2f}', '', ''])
    w.writerow(['', '', '', ''])
    w.writerow(['Benchmark', 'OR in model', '', ''])
    w.writerow(['SOFA (per point)', '1.16', '', 'Reference'])
    w.writerow(['Lactate (per mmol/L)', '1.14', '', 'Reference'])
    w.writerow(['CCI (per point)', '1.14', '', 'Reference'])
    w.writerow(['', '', '', ''])
    w.writerow(['Conclusion', '', '',
                f'E={ep:.1f} indicates substantial robustness. '
                f'Unmeasured confounder would need RR>{ep:.1f} — exceeding '
                f'established strong predictors (SOFA, lactate) — to explain away DSI.'])

print(f'Saved: {csv_path}')
print("Done!")
