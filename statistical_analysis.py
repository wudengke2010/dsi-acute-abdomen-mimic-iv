"""
Statistical analysis for Shock Index derived indicators in acute abdomen ICU patients.
Includes: descriptive stats, ROC/AUC comparison, logistic regression, subgroup analysis, DCA.
"""
import pandas as pd, numpy as np, os, sys
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

OUT = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'

# Load analysis dataset
df = pd.read_csv(os.path.join(OUT, 'analysis_dataset.csv'))
print(f'Analysis dataset: {len(df)} stays')
print(f'ICU death: {df["icu_death"].sum()} ({df["icu_death"].mean():.3f})')

# Filter: only stays with complete SI data
df_clean = df[df['SI_first'].notna() & df['MSI_first'].notna() & df['DSI_first'].notna()].copy()
print(f'Clean dataset (complete vitals): {len(df_clean)} stays')

# Remove extreme outliers for SI derivatives
for col in ['SI_first','SI_max','SI_mean','MSI_first','MSI_max','MSI_mean','DSI_first','DSI_max','DSI_mean','Age_SI_first','Age_SI_max','Age_SI_mean']:
    if col in df_clean.columns:
        q01, q99 = df_clean[col].quantile([0.01, 0.99])
        df_clean = df_clean[(df_clean[col] >= q01) & (df_clean[col] <= q99)]

print(f'After outlier removal: {len(df_clean)} stays')

# ============================================================
# SECTION 1: Descriptive Statistics (Table 1)
# ============================================================
print('\n' + '='*60)
print('TABLE 1: Baseline Characteristics')
print('='*60)

# Split by ICU death outcome
survived = df_clean[df_clean['icu_death'] == 0]
died = df_clean[df_clean['icu_death'] == 1]

table1_data = []

def add_continuous(var_name, var_col, df_surv, df_dead):
    """Add continuous variable to Table 1"""
    # Check normality
    _, p_norm_s = stats.shapiro(df_surv[var_col].dropna().sample(min(5000, len(df_surv[var_col].dropna())), random_state=42) if len(df_surv[var_col].dropna()) > 5000 else df_surv[var_col].dropna())
    _, p_norm_d = stats.shapiro(df_dead[var_col].dropna().sample(min(5000, len(df_dead[var_col].dropna())), random_state=42) if len(df_dead[var_col].dropna()) > 5000 else df_dead[var_col].dropna())

    if p_norm_s > 0.05 and p_norm_d > 0.05:
        # Normal distribution - use mean ± SD, t-test
        mean_s, mean_d = df_surv[var_col].mean(), df_dead[var_col].mean()
        sd_s, sd_d = df_surv[var_col].std(), df_dead[var_col].std()
        _, p_val = stats.ttest_ind(df_surv[var_col].dropna(), df_dead[var_col].dropna())
        val_surv = f'{mean_s:.1f} ± {sd_s:.1f}'
        val_dead = f'{mean_d:.1f} ± {sd_d:.1f}'
    else:
        # Non-normal - use median (IQR), Mann-Whitney
        med_s, med_d = df_surv[var_col].median(), df_dead[var_col].median()
        q1_s, q3_s = df_surv[var_col].quantile([0.25, 0.75])
        q1_d, q3_d = df_dead[var_col].quantile([0.25, 0.75])
        _, p_val = stats.mannwhitneyu(df_surv[var_col].dropna(), df_dead[var_col].dropna())
        val_surv = f'{med_s:.1f} ({q1_s:.1f}-{q3_s:.1f})'
        val_dead = f'{med_d:.1f} ({q1_d:.1f}-{q3_d:.1f})'

    table1_data.append({
        'Variable': var_name,
        'Survived (n={})'.format(len(df_surv)): val_surv,
        'Died (n={})'.format(len(df_dead)): val_dead,
        'P value': f'{p_val:.4f}' if p_val >= 0.001 else '<0.001'
    })

def add_categorical(var_name, var_col, df_surv, df_dead):
    """Add categorical variable to Table 1"""
    cats_s = df_surv[var_col].value_counts()
    cats_d = df_dead[var_col].value_counts()
    total_s = len(df_surv)
    total_d = len(df_dead)

    # Chi-square test
    contingency = pd.DataFrame({
        'Survived': cats_s,
        'Died': cats_d
    }).fillna(0)
    chi2, p_val, _, _ = stats.chi2_contingency(contingency)

    for cat in cats_s.index:
        n_s = cats_s.get(cat, 0)
        n_d = cats_d.get(cat, 0)
        table1_data.append({
            'Variable': f'{var_name} - {cat}',
            'Survived (n={})'.format(total_s): f'{n_s} ({n_s/total_s*100:.1f}%)',
            'Died (n={})'.format(total_d): f'{n_d} ({n_d/total_d*100:.1f}%)',
            'P value': f'{p_val:.4f}' if p_val >= 0.001 else '<0.001'
        })

# Continuous variables
add_continuous('Age (years)', 'age_at_admission', survived, died)
add_continuous('Heart Rate (first)', 'HR_first', survived, died)
add_continuous('SBP (first, mmHg)', 'SBP_first', survived, died)
add_continuous('DBP (first, mmHg)', 'DBP_first', survived, died)
add_continuous('MAP (first, mmHg)', 'MAP_first', survived, died)
add_continuous('Shock Index (first)', 'SI_first', survived, died)
add_continuous('Modified Shock Index (first)', 'MSI_first', survived, died)
add_continuous('Diastolic Shock Index (first)', 'DSI_first', survived, died)
add_continuous('Age-adjusted SI (first)', 'Age_SI_first', survived, died)
add_continuous('Shock Index (worst)', 'SI_max', survived, died)
add_continuous('Modified Shock Index (worst)', 'MSI_max', survived, died)
add_continuous('Diastolic Shock Index (worst)', 'DSI_max', survived, died)
add_continuous('Charlson Comorbidity Index', 'CCI', survived, died)
add_continuous('ICU LOS (days)', 'los', survived, died)

# Categorical variables
add_categorical('Gender', 'gender', survived, died)
add_categorical('Abdomen Subtype', 'abdomen_subtype', survived, died)

table1 = pd.DataFrame(table1_data)
table1.to_csv(os.path.join(OUT, 'table1_baseline.csv'), index=False)
print(table1.to_string())

# ============================================================
# SECTION 2: ROC/AUC Analysis
# ============================================================
print('\n' + '='*60)
print('SECTION 2: ROC/AUC Analysis')
print('='*60)

outcomes = {
    'ICU Mortality': 'icu_death',
    'Prolonged ICU Stay (>3d)': 'prolonged_icu',
}

predictors = {
    'SI (first)': 'SI_first',
    'SI (worst)': 'SI_max',
    'SI (mean)': 'SI_mean',
    'MSI (first)': 'MSI_first',
    'MSI (worst)': 'MSI_max',
    'MSI (mean)': 'MSI_mean',
    'DSI (first)': 'DSI_first',
    'DSI (worst)': 'DSI_max',
    'DSI (mean)': 'DSI_mean',
    'Age-SI (first)': 'Age_SI_first',
    'Age-SI (worst)': 'Age_SI_max',
}

auc_results = []

for outcome_name, outcome_col in outcomes.items():
    print(f'\n--- Outcome: {outcome_name} ---')
    y = df_clean[outcome_col]

    for pred_name, pred_col in predictors.items():
        x = df_clean[pred_col]
        mask = x.notna() & y.notna()
        if mask.sum() < 30:
            continue

        auc = roc_auc_score(y[mask], x[mask])
        fpr, tpr, thresholds = roc_curve(y[mask], x[mask])

        # Optimal cutoff (Youden index)
        youden = tpr - fpr
        best_idx = np.argmax(youden)
        best_threshold = thresholds[best_idx]
        sensitivity = tpr[best_idx]
        specificity = 1 - fpr[best_idx]

        # 95% CI for AUC (bootstrapping)
        n_boot = 1000
        boot_aucs = []
        for i in range(n_boot):
            idx_boot = np.random.choice(mask[mask].index, size=mask.sum(), replace=True)
            try:
                boot_auc = roc_auc_score(y[idx_boot], x[idx_boot])
                boot_aucs.append(boot_auc)
            except:
                continue
        auc_ci_low = np.percentile(boot_aucs, 2.5)
        auc_ci_high = np.percentile(boot_aucs, 97.5)

        auc_results.append({
            'Outcome': outcome_name,
            'Predictor': pred_name,
            'AUC': f'{auc:.3f}',
            '95% CI': f'{auc_ci_low:.3f}-{auc_ci_high:.3f}',
            'Best Cut-off': f'{best_threshold:.2f}',
            'Sensitivity': f'{sensitivity:.3f}',
            'Specificity': f'{specificity:.3f}',
            'Youden J': f'{youden[best_idx]:.3f}',
        })

        print(f'  {pred_name}: AUC={auc:.3f} ({auc_ci_low:.3f}-{auc_ci_high:.3f}), '
              f'Cut-off={best_threshold:.2f}, Sens={sensitivity:.3f}, Spec={specificity:.3f}')

# DeLong test for AUC comparison (using SI_first as reference)
print('\n--- AUC Pairwise Comparison (vs SI first) ---')
ref_pred = 'SI_first'
for outcome_name, outcome_col in outcomes.items():
    y = df_clean[outcome_col]
    x_ref = df_clean[ref_pred]
    mask_ref = x_ref.notna() & y.notna()
    auc_ref = roc_auc_score(y[mask_ref], x_ref[mask_ref])

    for pred_name, pred_col in predictors.items():
        if pred_name == ref_pred:
            continue
        x_comp = df_clean[pred_col]
        mask_both = x_ref.notna() & x_comp.notna() & y.notna()
        if mask_both.sum() < 30:
            continue

        auc_comp = roc_auc_score(y[mask_both], x_comp[mask_both])
        auc_ref_sub = roc_auc_score(y[mask_both], x_ref[mask_both])

        # Z-test for AUC comparison
        # Hanley & McNeil method
        n1 = y[mask_both].sum()  # positives
        n2 = mask_both.sum() - n1  # negatives
        q1 = auc_ref_sub / (2 - auc_comp)
        q2 = 2 * auc_comp**2 / (1 + auc_ref_sub)
        se = np.sqrt((auc_ref_sub*(1-auc_ref_sub)*(n1+n2-1) + (n1-1)*(q1-auc_ref_sub**2) + (n2-1)*(q2-auc_comp**2)) / (n1*n2))
        z = (auc_comp - auc_ref_sub) / se if se > 0 else 0
        p_val = 2 * (1 - stats.norm.cdf(abs(z)))

        print(f'  {outcome_name}: {pred_name} vs {ref_pred}: '
              f'AUC_diff={auc_comp-auc_ref_sub:.3f}, z={z:.3f}, p={p_val:.4f}')

auc_table = pd.DataFrame(auc_results)
auc_table.to_csv(os.path.join(OUT, 'table2_auc.csv'), index=False)
print(f'\nSaved AUC table to table2_auc.csv')

# ============================================================
# SECTION 3: Multivariable Logistic Regression
# ============================================================
print('\n' + '='*60)
print('SECTION 3: Multivariable Logistic Regression')
print('='*60)

# Model 1: SI only + covariates
# Model 2: MSI only + covariates
# Model 3: DSI only + covariates
# Model 4: Age-SI only + covariates
# Model 5: All SI derivatives + covariates (full model)

covariates = ['age_at_admission', 'gender', 'CCI']
# Encode gender
df_clean['gender_enc'] = (df_clean['gender'] == 'M').astype(int)

for outcome_name, outcome_col in [('ICU Mortality', 'icu_death'), ('Prolonged ICU Stay', 'prolonged_icu')]:
    print(f'\n--- Outcome: {outcome_name} ---')
    y = df_clean[outcome_col]

    for model_name, predictors_list in [
        ('SI model', ['SI_first']),
        ('MSI model', ['MSI_first']),
        ('DSI model', ['DSI_first']),
        ('Age-SI model', ['Age_SI_first']),
        ('Full model (all SI derivatives)', ['SI_first', 'MSI_first', 'DSI_first', 'Age_SI_first']),
        ('Covariates only', []),
    ]:
        X_cols = predictors_list + ['age_at_admission', 'gender_enc', 'CCI']
        X = df_clean[X_cols].copy()
        X = sm.add_constant(X)
        mask = X.notna().all(axis=1) & y.notna()

        try:
            model = sm.Logit(y[mask], X[mask]).fit(disp=0, maxiter=100)
            print(f'\n  {model_name}:')
            print(f'    AIC={model.aic:.1f}, BIC={model.bic:.1f}')
            print(f'    Likelihood ratio p={model.llr_pvalue:.4f}')
            for col in X_cols:
                if col in model.params.index:
                    coef = model.params[col]
                    p = model.pvalues[col]
                    or_val = np.exp(coef)
                    ci_low = np.exp(coef - 1.96 * model.bse[col])
                    ci_high = np.exp(coef + 1.96 * model.bse[col])
                    print(f'    {col}: OR={or_val:.3f} ({ci_low:.3f}-{ci_high:.3f}), p={p:.4f}')

            # Model AUC
            pred_proba = model.predict(X[mask])
            auc_model = roc_auc_score(y[mask], pred_proba)
            print(f'    Model AUC={auc_model:.3f}')
        except Exception as e:
            print(f'  {model_name}: Error - {e}')

# ============================================================
# SECTION 4: Subgroup Analysis
# ============================================================
print('\n' + '='*60)
print('SECTION 4: Subgroup Analysis by Abdomen Subtype')
print('='*60)

for subtype in df_clean['abdomen_subtype'].unique():
    sub_df = df_clean[df_clean['abdomen_subtype'] == subtype]
    if len(sub_df) < 20:
        continue

    y = sub_df['icu_death']
    print(f'\n--- Subtype: {subtype} (n={len(sub_df)}, deaths={y.sum()}) ---')

    for pred_name, pred_col in [('SI', 'SI_first'), ('MSI', 'MSI_first'), ('DSI', 'DSI_first'), ('Age-SI', 'Age_SI_first')]:
        mask = sub_df[pred_col].notna() & y.notna()
        if mask.sum() < 20:
            continue
        auc = roc_auc_score(y[mask], sub_df[pred_col][mask])
        print(f'  {pred_name}: AUC={auc:.3f}')

# ============================================================
# SECTION 5: Composite Shock Index (CSI) - Novel Index
# ============================================================
print('\n' + '='*60)
print('SECTION 5: Composite Shock Index (CSI)')
print('='*60)

# CSI = weighted combination of SI derivatives
# Use logistic regression coefficients as weights

y = df_clean['icu_death']
X_csi = df_clean[['SI_first', 'MSI_first', 'DSI_first', 'Age_SI_first']].copy()
mask = X_csi.notna().all(axis=1) & y.notna()

model_csi = sm.Logit(y[mask], sm.add_constant(X_csi[mask])).fit(disp=0)

# Get standardized coefficients
coefs = model_csi.params[['SI_first', 'MSI_first', 'DSI_first', 'Age_SI_first']]
stds = X_csi[mask].std()
std_coefs = coefs * stds

# CSI = weighted sum of standardized values
weights = std_coefs / std_coefs.sum()  # normalize to sum=1
print(f'CSI weights: {weights.to_dict()}')

df_clean_csi = df_clean[mask].copy()
df_clean_csi['CSI'] = (
    weights['SI_first'] * (df_clean_csi['SI_first'] - df_clean_csi['SI_first'].mean()) / df_clean_csi['SI_first'].std() +
    weights['MSI_first'] * (df_clean_csi['MSI_first'] - df_clean_csi['MSI_first'].mean()) / df_clean_csi['MSI_first'].std() +
    weights['DSI_first'] * (df_clean_csi['DSI_first'] - df_clean_csi['DSI_first'].mean()) / df_clean_csi['DSI_first'].std() +
    weights['Age_SI_first'] * (df_clean_csi['Age_SI_first'] - df_clean_csi['Age_SI_first'].mean()) / df_clean_csi['Age_SI_first'].std()
)

auc_csi = roc_auc_score(df_clean_csi['icu_death'], df_clean_csi['CSI'])
print(f'CSI AUC for ICU mortality: {auc_csi:.3f}')

# ============================================================
# SECTION 6: Decision Curve Analysis (DCA)
# ============================================================
print('\n' + '='*60)
print('SECTION 6: Decision Curve Analysis')
print('='*60)

threshold_range = np.arange(0.01, 0.50, 0.01)

def compute_net_benefit(y_true, y_pred_proba, thresholds):
    """Compute net benefit for DCA"""
    net_benefits = []
    for t in thresholds:
        tp = ((y_pred_proba >= t) & (y_true == 1)).sum()
        fp = ((y_pred_proba >= t) & (y_true == 0)).sum()
        n = len(y_true)
        nb = tp/n - fp/n * (t / (1-t))
        net_benefits.append(nb)
    return net_benefits

y = df_clean['icu_death']

# Compute net benefit for each predictor model
for pred_name, pred_col in [('SI', 'SI_first'), ('MSI', 'MSI_first'), ('DSI', 'DSI_first'), ('Age-SI', 'Age_SI_first')]:
    mask = df_clean[pred_col].notna() & y.notna()
    # Fit simple logistic model
    X = sm.add_constant(df_clean[mask][[pred_col]])
    model = sm.Logit(y[mask], X).fit(disp=0)
    pred_proba = model.predict(X)
    nb = compute_net_benefit(y[mask].values, pred_proba.values, threshold_range)
    print(f'{pred_name}: max NB={max(nb):.3f} at threshold={threshold_range[np.argmax(nb)]:.2f}')

# Also compute CSI net benefit
mask_csi = df_clean_csi['CSI'].notna() & df_clean_csi['icu_death'].notna()
X_csi_dca = sm.add_constant(df_clean_csi[['CSI']])
model_csi_dca = sm.Logit(df_clean_csi['icu_death'], X_csi_dca).fit(disp=0)
pred_proba_csi = model_csi_dca.predict(X_csi_dca)
nb_csi = compute_net_benefit(df_clean_csi['icu_death'].values, pred_proba_csi.values, threshold_range)
print(f'CSI: max NB={max(nb_csi):.3f} at threshold={threshold_range[np.argmax(nb_csi)]:.2f}')

# ============================================================
# SECTION 7: Summary Results
# ============================================================
print('\n' + '='*60)
print('SUMMARY OF KEY FINDINGS')
print('='*60)

# Find best predictor for each outcome
for outcome_name, outcome_col in [('ICU Mortality', 'icu_death'), ('Prolonged ICU Stay', 'prolonged_icu')]:
    outcome_auc = auc_table[auc_table['Outcome'] == outcome_name]
    best_row = outcome_auc.loc[outcome_auc['AUC'].astype(float).idxmax()]
    print(f'{outcome_name}: Best predictor = {best_row["Predictor"]} (AUC={best_row["AUC"]})')

print(f'CSI AUC for ICU mortality: {auc_csi:.3f}')
print(f'Subgroup analysis completed for {len(df_clean["abdomen_subtype"].unique())} subtypes')

# Save clean dataset
df_clean.to_csv(os.path.join(OUT, 'analysis_dataset_clean.csv'), index=False)
print(f'\nSaved clean analysis dataset: {len(df_clean)} stays')
