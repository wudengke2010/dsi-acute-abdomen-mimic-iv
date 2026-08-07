"""
Standalone script: Regenerate Fig5 Calibration with 2x2 portrait layout (Fig.6-inspired).
Only outputs PNG to avoid fontTools DLL issues with PDF/SVG backends.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score
from scipy.stats import chi2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Colorblind-safe palette (Wong 2011)
C = {
    'blue': '#0072B2',
    'orange': '#D55E00',
    'gray': '#999999',
}

OUTPUT_DIR = "C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen/figures"
DATA_PATH = "C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen/analysis_dataset_revised.csv"

# Load data
df = pd.read_csv(DATA_PATH)
cc = df.copy()
y = cc['hospital_expire_flag'].values
N = len(cc)

# Prepare model matrices
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

# Fit all models
print("Fitting models...")
m_basic = sm.Logit(y, get_X_basic()).fit(disp=0, maxiter=5000)
m_ext = sm.Logit(y, get_X_extended()).fit(disp=0, maxiter=5000)
m_ext_dsi = sm.Logit(y, get_X_extended_dsi()).fit(disp=0, maxiter=5000)
m_ext_all = sm.Logit(y, get_X_extended_all_si()).fit(disp=0, maxiter=5000)

p_basic = m_basic.predict(get_X_basic())
p_ext = m_ext.predict(get_X_extended())
p_ext_dsi = m_ext_dsi.predict(get_X_extended_dsi())
p_ext_all = m_ext_all.predict(get_X_extended_all_si())

print(f"AUCs: basic={roc_auc_score(y,p_basic):.4f}, ext={roc_auc_score(y,p_ext):.4f}, "
      f"ext_dsi={roc_auc_score(y,p_ext_dsi):.4f}, ext_all={roc_auc_score(y,p_ext_all):.4f}")

# Hosmer-Lemeshow test
def hosmer_lemeshow(y_true, y_pred, g=10):
    pred_series = pd.Series(y_pred)
    y_s = pd.Series(y_true)
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
    df_val = max(1, n_groups - 2)
    p_value = 1 - chi2.cdf(chi_sq, df_val) if chi_sq > 0 else 1.0
    return chi_sq, p_value

# ============================================================
# Fig 5: Calibration Plots — 2x2 portrait layout (Fig.6-inspired)
# ============================================================
print("Generating Fig 5: Calibration (2x2 portrait, Fig.6-inspired)...")

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

predictions = [
    ('Basic baseline', p_basic),
    ('Extended +SOFA', p_ext),
    ('Extended +SOFA +DSI', p_ext_dsi),
    ('Extended +SOFA +all SI', p_ext_all),
]

# Big bold overall title — mirrors Fig.6's title style
fig.suptitle('Calibration Plots: Predicted vs Observed In-Hospital Mortality',
             fontsize=14, fontweight='bold', y=0.98)

y_series = pd.Series(y, name='outcome')

for idx, (label, pred) in enumerate(predictions):
    row, col = idx // 2, idx % 2
    ax = axes[row, col]

    # Highlight the key panel (Ext+SOFA+DSI) — mirrors Fig.6's DSI highlight
    if 'DSI' in label and 'all' not in label:
        ax.set_facecolor('#FFF5E6')  # light orange tint
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

    # Axis labels only on outer edges (clean, like Fig.6)
    if col == 0:
        ax.set_ylabel('Observed Rate', fontsize=11)
    if row == 1:
        ax.set_xlabel('Predicted Probability', fontsize=11)

    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.set_xlim([0, 0.6])
    ax.set_ylim([0, 0.6])
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')

    # Brier + HL P-value annotation box (like Fig.6's annotation column)
    brier = np.mean((pred_series - y_series)**2)
    _, hl_p = hosmer_lemeshow(y, pred)
    hl_str = f'{hl_p:.3f}' if hl_p >= 0.001 else f'{hl_p:.2e}'
    textstr = f'Brier={brier:.4f}\nHL P={hl_str}'
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
            fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(f'{OUTPUT_DIR}/Fig5_Calibration.png', dpi=300, bbox_inches='tight')
print(f"Saved: {OUTPUT_DIR}/Fig5_Calibration.png")
plt.close()
print("Done.")
