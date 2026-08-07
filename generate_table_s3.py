import pandas as pd, numpy as np

df = pd.read_csv('analysis_dataset_corrected.csv')
df['gender_male'] = (df['gender'] == 'M').astype(int)
model_vars = ['age_at_admission', 'gender_male', 'CCI', 'lactate_first', 'wbc_first',
              'vasopressor_use', 'any_surgery', 'mechanical_ventilation', 'SI_mean',
              'MSI_mean', 'DSI_mean', 'Age_SI_mean', 'hospital_expire_flag',
              'icu_death_strict', 'los', 'abdomen_subtype']
df_cc = df[model_vars].dropna()

def median_iqr(x):
    return f'{x.median():.1f} [{x.quantile(0.25):.1f}-{x.quantile(0.75):.1f}]'

df_cc['DSI_Q'] = pd.qcut(df_cc['DSI_mean'], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'])

quartiles = ['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)']
rows = []

def add_row(label, overall_func, quartile_func):
    row = [label, overall_func(df_cc)]
    for q in quartiles:
        row.append(quartile_func(df_cc[df_cc['DSI_Q'] == q]))
    rows.append(row)

add_row('Age, years', lambda x: median_iqr(x['age_at_admission']), lambda s: median_iqr(s['age_at_admission']))
add_row('Male, n (%)', lambda x: f"{x['gender_male'].sum()} ({x['gender_male'].mean()*100:.1f}%)", lambda s: f"{s['gender_male'].sum()} ({s['gender_male'].mean()*100:.1f}%)")
add_row('CCI', lambda x: median_iqr(x['CCI']), lambda s: median_iqr(s['CCI']))
add_row('Lactate, mmol/L', lambda x: median_iqr(x['lactate_first']), lambda s: median_iqr(s['lactate_first']))
add_row('WBC, ×10⁹/L', lambda x: median_iqr(x['wbc_first']), lambda s: median_iqr(s['wbc_first']))
add_row('Vasopressor use, n (%)', lambda x: f"{x['vasopressor_use'].sum()} ({x['vasopressor_use'].mean()*100:.1f}%)", lambda s: f"{s['vasopressor_use'].sum()} ({s['vasopressor_use'].mean()*100:.1f}%)")
add_row('Surgery, n (%)', lambda x: f"{x['any_surgery'].sum()} ({x['any_surgery'].mean()*100:.1f}%)", lambda s: f"{s['any_surgery'].sum()} ({s['any_surgery'].mean()*100:.1f}%)")
add_row('Mechanical ventilation, n (%)', lambda x: f"{x['mechanical_ventilation'].sum()} ({x['mechanical_ventilation'].mean()*100:.1f}%)", lambda s: f"{s['mechanical_ventilation'].sum()} ({s['mechanical_ventilation'].mean()*100:.1f}%)")
add_row('ICU LOS, days', lambda x: median_iqr(x['los']), lambda s: median_iqr(s['los']))
add_row('In-hospital mortality, n (%)', lambda x: f"{x['hospital_expire_flag'].sum()} ({x['hospital_expire_flag'].mean()*100:.1f}%)", lambda s: f"{s['hospital_expire_flag'].sum()} ({s['hospital_expire_flag'].mean()*100:.1f}%)")
add_row('ICU mortality, n (%)', lambda x: f"{x['icu_death_strict'].sum()} ({x['icu_death_strict'].mean()*100:.1f}%)", lambda s: f"{s['icu_death_strict'].sum()} ({s['icu_death_strict'].mean()*100:.1f}%)")

for st in ['inflammation', 'obstruction', 'perforation', 'ischemia', 'other']:
    n = (df_cc['abdomen_subtype'] == st).sum()
    row = [f'Subtype: {st.capitalize()}, n (%)', f'{n} ({n/len(df_cc)*100:.1f}%)']
    for q in quartiles:
        sub = df_cc[df_cc['DSI_Q'] == q]
        n_q = (sub['abdomen_subtype'] == st).sum()
        row.append(f'{n_q} ({n_q/len(sub)*100:.1f}%)')
    rows.append(row)

cols = ['Characteristic', 'Overall (N=5,728)', 'Q1 (Low, n=1,432)', 'Q2 (n=1,432)', 'Q3 (n=1,432)', 'Q4 (High, n=1,432)']
s3 = pd.DataFrame(rows, columns=cols)
s3.to_csv('Table_S3_Baseline_Characteristics.csv', index=False)
print('Saved Table_S3_Baseline_Characteristics.csv')
