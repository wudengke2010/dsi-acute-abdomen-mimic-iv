"""Verify claim: 'DSI was the strongest SI derivative' — univariable and adjusted comparisons."""
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm

df = pd.read_csv("analysis_dataset_with_sofa.csv")
y = df["hospital_expire_flag"].values

base_cols = ["age_at_admission", "gender_binary", "CCI", "lactate_first",
             "wbc_first", "vasopressor_use", "any_surgery_during_hospitalization", "sofa_total"]
# check column availability
for c in base_cols + ["mv_or_niv"]:
    pass

# identify actual covariate columns
cand = {"age": "age_at_admission", "sex": "gender_binary", "cci": "CCI",
        "lactate": "lactate_first", "wbc": "wbc_first",
        "vaso": "vasopressor_use", "mv": "mv_or_niv", "sofa": "sofa_total"}
for k, v in cand.items():
    if v not in df.columns:
        print("MISSING:", v)
print("columns sample:", [c for c in df.columns if c in cand.values()])

# --- Univariable AUCs (mean 24h) ---
print("\n--- Univariable AUC (in-hospital mortality) ---")
for col in ["SI_mean", "MSI_mean", "DSI_mean", "Age_SI_mean"]:
    sub = df[[col]].dropna()
    m = sub.index
    auc = roc_auc_score(y[m], df.loc[m, col])
    print(f"{col:12s} AUC={auc:.4f}  (n={len(m)})")

# --- Adjusted models: baseline + each derivative ---
print("\n--- Extended baseline (no surgery) + each derivative ---")
cov = ["age_at_admission", "gender", "CCI", "lactate_first",
       "wbc_first", "vasopressor_use", "mechanical_ventilation", "sofa"]
data = df[cov + ["SI_mean", "MSI_mean", "DSI_mean", "Age_SI_mean", "hospital_expire_flag"]].dropna().copy()
data["gender"] = (data["gender"] == "M").astype(float)
y2 = data["hospital_expire_flag"].values
Xb = sm.add_constant(data[cov].astype(float))
m0 = sm.GLM(y2, Xb, family=sm.families.Binomial()).fit()
p0 = m0.predict(Xb)
auc0 = roc_auc_score(y2, p0)
print(f"Baseline AUC = {auc0:.4f}")

from scipy.stats import norm

def delong_var_diff(y, p1, p2):
    """Variance of AUC(p1) - AUC(p2) on same sample (paired DeLong)."""
    y = np.asarray(y); p1 = np.asarray(p1); p2 = np.asarray(p2)
    n1 = int(y.sum()); n0 = len(y) - n1
    def struct(p):
        s1 = p[y == 1]; s0 = p[y == 0]
        v10 = (s1[:, None] > s0[None, :]).mean(axis=1)  # per case
        v01 = (s0[:, None] < s1[None, :]).mean(axis=1)  # per control
        return v10, v01
    V10a, V01a = struct(p1)
    V10b, V01b = struct(p2)
    var10 = np.var(V10a - V10b)
    var01 = np.var(V01a - V01b)
    return var10 / n1 + var01 / n0

for col in ["SI_mean", "MSI_mean", "DSI_mean", "Age_SI_mean"]:
    X = sm.add_constant(data[cov + [col]].astype(float))
    m = sm.GLM(y2, X, family=sm.families.Binomial()).fit()
    p = m.predict(X)
    auc = roc_auc_score(y2, p)
    delta = auc - auc0
    var = delong_var_diff(y2, p0, p)
    z = delta / np.sqrt(var)
    pv = 2 * (1 - norm.cdf(abs(z)))
    orr = np.exp(m.params[col])
    ci = np.exp(m.conf_int().loc[col])
    print(f"+{col:12s} AUC={auc:.4f} dAUC={delta:+.4f} DeLong z={z:.2f} P={pv:.4f}  OR={orr:.2f} ({ci[0]:.2f}-{ci[1]:.2f})  Pcoef={m.pvalues[col]:.2e}")
