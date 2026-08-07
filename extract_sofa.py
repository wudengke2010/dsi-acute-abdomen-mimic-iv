"""
Extract first-day SOFA scores for the CC cohort from MIMIC-IV v3.1.
Uses DuckDB to query CSV.gz files directly.
Time window: 6h before ICU admission to 24h after (per first_day_sofa.sql convention).
"""
import pandas as pd
import numpy as np
import duckdb
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = "E:/mimic-iv/v3.1/physionet.org/files/mimiciv/3.1"
HOSP_DIR = f"{DATA_DIR}/hosp"
ICU_DIR = f"{DATA_DIR}/icu"
OUTPUT_DIR = "C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen"

# Load CC cohort stay_ids
df = pd.read_csv(f"{OUTPUT_DIR}/analysis_dataset_corrected.csv")
cc = df[df['lactate_first'].notna() & df['wbc_first'].notna()].copy()
stay_ids = cc['stay_id'].unique().tolist()
hadm_ids = cc['hadm_id'].unique().tolist()
subject_ids = cc['subject_id'].unique().tolist()

print(f"CC cohort: {len(cc)} stays, {len(hadm_ids)} admissions, {len(subject_ids)} subjects")

# Create DuckDB connection
con = duckdb.connect()

# Register stay_ids as a temp table
cc_ids = pd.DataFrame({'stay_id': stay_ids, 'hadm_id': cc['hadm_id'].values, 'subject_id': cc['subject_id'].values})
con.register('cc_ids', cc_ids)

# Step 1: Get icustays intime/outtime
print("\n[1/7] Loading icustays...")
icustays = con.execute(f"""
    SELECT stay_id, subject_id, hadm_id, intime, outtime
    FROM read_csv_auto('{ICU_DIR}/icustays.csv.gz')
    WHERE stay_id IN (SELECT stay_id FROM cc_ids)
""").fetchdf()
print(f"  icustays: {len(icustays)} rows")

# Step 2: Query labevents for platelets, bilirubin, creatinine, PaO2
print("[2/7] Querying labevents for platelets, bilirubin, creatinine, PaO2...")
# itemids: 51265=platelet, 50885=bilirubin_total, 50912=creatinine, 50821=PaO2
lab_itemids = [51265, 50885, 50912, 50821]
lab_str = ",".join([str(i) for i in lab_itemids])

lab = con.execute(f"""
    SELECT le.subject_id, le.hadm_id, le.charttime, le.itemid, le.valuenum
    FROM read_csv_auto('{HOSP_DIR}/labevents.csv.gz') le
    INNER JOIN (SELECT DISTINCT subject_id FROM cc_ids) ci
        ON le.subject_id = ci.subject_id
    WHERE le.itemid IN ({lab_str})
      AND le.valuenum IS NOT NULL
""").fetchdf()
print(f"  labevents (filtered): {len(lab)} rows")

# Step 3: Query chartevents for GCS, FiO2, MAP
print("[3/7] Querying chartevents for GCS, FiO2, MAP...")
# GCS: 220739=motor, 223900=verbal, 223901=eyes
# FiO2: 223835, 190
# MAP: 220052, 220181, 456, 52, 6702, 443, 132051, 224326
chart_itemids = [220739, 223900, 223901, 223835, 190, 220052, 220181, 456, 52, 6702, 443, 132051, 224326]
chart_str = ",".join([str(i) for i in chart_itemids])

chart = con.execute(f"""
    SELECT ce.stay_id, ce.charttime, ce.itemid, ce.valuenum
    FROM read_csv_auto('{ICU_DIR}/chartevents.csv.gz') ce
    INNER JOIN (SELECT stay_id FROM cc_ids) ci
        ON ce.stay_id = ci.stay_id
    WHERE ce.itemid IN ({chart_str})
      AND ce.valuenum IS NOT NULL
""").fetchdf()
print(f"  chartevents (filtered): {len(chart)} rows")

# Step 4: Query outputevents for urine output
print("[4/7] Querying outputevents for urine output...")
# Urine output itemids
uo_itemids = [226559, 226560, 226561, 226584, 226565, 226567, 226558, 227489, 226566, 226627]
uo_str = ",".join([str(i) for i in uo_itemids])

uo = con.execute(f"""
    SELECT oe.stay_id, oe.charttime, oe.itemid, oe.value AS valuenum
    FROM read_csv_auto('{ICU_DIR}/outputevents.csv.gz') oe
    INNER JOIN (SELECT stay_id FROM cc_ids) ci
        ON oe.stay_id = ci.stay_id
    WHERE oe.itemid IN ({uo_str})
      AND oe.value IS NOT NULL
""").fetchdf()
print(f"  outputevents (filtered): {len(uo)} rows")

# Step 5: Query inputevents for vasopressor rates
print("[5/7] Querying inputevents for vasopressor rates...")
# Norepinephrine: 221906, Epinephrine: 221289, Dopamine: 221662, Dobutamine: 221653
vaso_itemids = [221906, 221289, 221662, 221653]
vaso_str = ",".join([str(i) for i in vaso_itemids])

vaso = con.execute(f"""
    SELECT ie.stay_id, ie.starttime, ie.endtime, ie.itemid, ie.rate
    FROM read_csv_auto('{ICU_DIR}/inputevents.csv.gz') ie
    INNER JOIN (SELECT stay_id FROM cc_ids) ci
        ON ie.stay_id = ci.stay_id
    WHERE ie.itemid IN ({vaso_str})
      AND ie.rate IS NOT NULL
""").fetchdf()
print(f"  inputevents (filtered): {len(vaso)} rows")

con.close()

# Step 6: Compute SOFA components
print("[6/7] Computing SOFA components...")

# Merge icustays with lab/chart/uo/vaso
icustays['intime'] = pd.to_datetime(icustays['intime'])
icustays['outtime'] = pd.to_datetime(icustays['outtime'])
icustays['window_start'] = icustays['intime'] - pd.Timedelta(hours=6)
icustays['window_end'] = icustays['intime'] + pd.Timedelta(hours=24)

# --- Lab components ---
lab['charttime'] = pd.to_datetime(lab['charttime'])
lab = lab.merge(icustays[['stay_id', 'hadm_id', 'window_start', 'window_end']].rename(columns={'stay_id': 'stay_id_lab'}),
                left_on='hadm_id', right_on='hadm_id', how='inner')
lab = lab[(lab['charttime'] >= lab['window_start']) & (lab['charttime'] <= lab['window_end'])]

# Platelets (51265) - use min
plt = lab[lab['itemid'] == 51265].groupby('hadm_id')['valuenum'].min().reset_index()
plt.columns = ['hadm_id', 'platelet_min']

# Bilirubin (50885) - use max
bili = lab[lab['itemid'] == 50885].groupby('hadm_id')['valuenum'].max().reset_index()
bili.columns = ['hadm_id', 'bilirubin_max']

# Creatinine (50912) - use max
cr = lab[lab['itemid'] == 50912].groupby('hadm_id')['valuenum'].max().reset_index()
cr.columns = ['hadm_id', 'creatinine_max_lab']

# PaO2 (50821)
pao2 = lab[lab['itemid'] == 50821].groupby('hadm_id')['valuenum'].min().reset_index()
pao2.columns = ['hadm_id', 'pao2_min']

print(f"  Platelets: {len(plt)} patients")
print(f"  Bilirubin: {len(bili)} patients")
print(f"  Creatinine (lab): {len(cr)} patients")
print(f"  PaO2: {len(pao2)} patients")

# --- Chart components ---
chart['charttime'] = pd.to_datetime(chart['charttime'])
chart = chart.merge(icustays[['stay_id', 'window_start', 'window_end']], on='stay_id', how='inner')
chart = chart[(chart['charttime'] >= chart['window_start']) & (chart['charttime'] <= chart['window_end'])]

# GCS - compute total GCS, then take min
gcs_motor = chart[chart['itemid'] == 220739][['stay_id', 'charttime', 'valuenum']].rename(columns={'valuenum': 'gcs_motor'})
gcs_verbal = chart[chart['itemid'] == 223900][['stay_id', 'charttime', 'valuenum']].rename(columns={'valuenum': 'gcs_verbal'})
gcs_eyes = chart[chart['itemid'] == 223901][['stay_id', 'charttime', 'valuenum']].rename(columns={'valuenum': 'gcs_eyes'})

# Merge GCS components on stay_id + closest charttime
gcs = gcs_motor.merge(gcs_verbal, on=['stay_id', 'charttime'], how='outer')
gcs = gcs.merge(gcs_eyes, on=['stay_id', 'charttime'], how='outer')
gcs['gcs_total'] = gcs[['gcs_motor', 'gcs_verbal', 'gcs_eyes']].sum(axis=1, min_count=1)
gcs_min = gcs[gcs['gcs_total'].notna()].groupby('stay_id')['gcs_total'].min().reset_index()
gcs_min.columns = ['stay_id', 'gcs_min']
print(f"  GCS: {len(gcs_min)} patients")

# FiO2
fio2 = chart[chart['itemid'].isin([223835, 190])].groupby('stay_id')['valuenum'].min().reset_index()
fio2.columns = ['stay_id', 'fio2_min']

# PaO2/FiO2 ratio - need to match pao2 (hadm_id) with fio2 (stay_id) via icustays
pao2_with_stay = pao2.merge(icustays[['stay_id', 'hadm_id']], on='hadm_id', how='inner')
pafi = pao2_with_stay.merge(fio2, on='stay_id', how='inner')
# Filter out unreasonable FiO2 values
pafi = pafi[(pafi['fio2_min'] > 0) & (pafi['fio2_min'] <= 100)]
pafi['pao2fio2'] = pafi['pao2_min'] / (pafi['fio2_min'] / 100)
pafi = pafi[['hadm_id', 'stay_id', 'pao2fio2']].rename(columns={'pao2fio2': 'pao2fio2ratio'})
# Keep the min ratio per patient
pafi = pafi.loc[pafi.groupby('hadm_id')['pao2fio2ratio'].idxmin()]
pafi = pafi[['hadm_id', 'pao2fio2ratio']]
print(f"  PaO2/FiO2: {len(pafi)} patients")

# MAP min from chartevents (use 220052, 220181, etc.)
map_data = chart[chart['itemid'].isin([220052, 220181, 456, 52, 6702, 443, 132051, 224326])]
map_min = map_data.groupby('stay_id')['valuenum'].min().reset_index()
map_min.columns = ['stay_id', 'map_min_chart']
print(f"  MAP (chart): {len(map_min)} patients")

# --- Urine output ---
uo['charttime'] = pd.to_datetime(uo['charttime'])
uo = uo.merge(icustays[['stay_id', 'window_start', 'window_end']], on='stay_id', how='inner')
uo = uo[(uo['charttime'] >= uo['window_start']) & (uo['charttime'] <= uo['window_end'])]
uo_total = uo.groupby('stay_id')['valuenum'].sum().reset_index()
uo_total.columns = ['stay_id', 'urineoutput']
print(f"  Urine output: {len(uo_total)} patients")

# --- Vasopressor rates ---
vaso['starttime'] = pd.to_datetime(vaso['starttime'])
vaso['endtime'] = pd.to_datetime(vaso['endtime'])
vaso = vaso.merge(icustays[['stay_id', 'window_start', 'window_end']], on='stay_id', how='inner')
vaso = vaso[(vaso['starttime'] >= vaso['window_start']) & (vaso['starttime'] <= vaso['window_end'])]

# Get max rate for each vasopressor
nor_rate = vaso[vaso['itemid'] == 221906].groupby('stay_id')['rate'].max().reset_index()
nor_rate.columns = ['stay_id', 'rate_norepinephrine']
epi_rate = vaso[vaso['itemid'] == 221289].groupby('stay_id')['rate'].max().reset_index()
epi_rate.columns = ['stay_id', 'rate_epinephrine']
dop_rate = vaso[vaso['itemid'] == 221662].groupby('stay_id')['rate'].max().reset_index()
dop_rate.columns = ['stay_id', 'rate_dopamine']
dob_rate = vaso[vaso['itemid'] == 221653].groupby('stay_id')['rate'].max().reset_index()
dob_rate.columns = ['stay_id', 'rate_dobutamine']

print(f"  Norepinephrine: {len(nor_rate)}, Epinephrine: {len(epi_rate)}, Dopamine: {len(dop_rate)}, Dobutamine: {len(dob_rate)}")

# Step 7: Assemble SOFA
print("[7/7] Assembling SOFA scores...")

sofa_df = icustays[['stay_id', 'hadm_id']].copy()

# Merge all components
sofa_df = sofa_df.merge(plt, on='hadm_id', how='left')
sofa_df = sofa_df.merge(bili, on='hadm_id', how='left')
sofa_df = sofa_df.merge(cr, on='hadm_id', how='left')
sofa_df = sofa_df.merge(gcs_min, on='stay_id', how='left')
sofa_df = sofa_df.merge(uo_total, on='stay_id', how='left')
sofa_df = sofa_df.merge(nor_rate, on='stay_id', how='left')
sofa_df = sofa_df.merge(epi_rate, on='stay_id', how='left')
sofa_df = sofa_df.merge(dop_rate, on='stay_id', how='left')
sofa_df = sofa_df.merge(dob_rate, on='stay_id', how='left')
sofa_df = sofa_df.merge(map_min, on='stay_id', how='left')

# Use existing dataset creatinine if lab creatinine missing
cc_cr = cc[['stay_id', 'cr_max']].copy()
sofa_df = sofa_df.merge(cc_cr, on='stay_id', how='left')
sofa_df['creatinine_final'] = sofa_df['creatinine_max_lab'].fillna(sofa_df['cr_max'])

# Use existing MAP_min from dataset
cc_map = cc[['stay_id', 'MAP_min']].copy()
sofa_df = sofa_df.merge(cc_map, on='stay_id', how='left')
sofa_df['map_final'] = sofa_df['map_min_chart'].fillna(sofa_df['MAP_min'])

# Use existing mechanical_ventilation for vent status
cc_mv = cc[['stay_id', 'mechanical_ventilation']].copy()
sofa_df = sofa_df.merge(cc_mv, on='stay_id', how='left')

# PaO2/FiO2 - merge
sofa_df = sofa_df.merge(pafi, on='hadm_id', how='left')

# --- Compute SOFA components ---
# Respiration
sofa_df['respiration'] = np.where(
    (sofa_df['mechanical_ventilation'] == 1) & (sofa_df['pao2fio2ratio'] < 100), 4,
    np.where(
        (sofa_df['mechanical_ventilation'] == 1) & (sofa_df['pao2fio2ratio'] < 200), 3,
        np.where(
            sofa_df['pao2fio2ratio'] < 300, 2,
            np.where(
                sofa_df['pao2fio2ratio'] < 400, 1,
                0
            )
        )
    )
)
# If pao2fio2ratio is NaN, respiration = 0 (per convention, missing = normal)
sofa_df['respiration'] = sofa_df['respiration'].fillna(0)

# Coagulation
sofa_df['coagulation'] = np.where(
    sofa_df['platelet_min'] < 20, 4,
    np.where(
        sofa_df['platelet_min'] < 50, 3,
        np.where(
            sofa_df['platelet_min'] < 100, 2,
            np.where(
                sofa_df['platelet_min'] < 150, 1,
                0
            )
        )
    )
)
sofa_df['coagulation'] = sofa_df['coagulation'].fillna(0)

# Liver
sofa_df['liver'] = np.where(
    sofa_df['bilirubin_max'] >= 12.0, 4,
    np.where(
        sofa_df['bilirubin_max'] >= 6.0, 3,
        np.where(
            sofa_df['bilirubin_max'] >= 2.0, 2,
            np.where(
                sofa_df['bilirubin_max'] >= 1.2, 1,
                0
            )
        )
    )
)
sofa_df['liver'] = sofa_df['liver'].fillna(0)

# Cardiovascular
sofa_df['cardiovascular'] = 0
# Score 4: dopamine >15, epi >0.1, nor >0.1
mask4 = (sofa_df['rate_dopamine'] > 15) | (sofa_df['rate_epinephrine'] > 0.1) | (sofa_df['rate_norepinephrine'] > 0.1)
sofa_df.loc[mask4.fillna(False), 'cardiovascular'] = 4
# Score 3: dopamine >5, epi <=0.1, nor <=0.1
mask3 = ((sofa_df['rate_dopamine'] > 5) | (sofa_df['rate_epinephrine'] <= 0.1) | (sofa_df['rate_norepinephrine'] <= 0.1)) & (sofa_df['cardiovascular'] < 4)
# Actually, the logic is: if any vaso present (not score 4), check for score 3
has_vaso = sofa_df[['rate_norepinephrine', 'rate_epinephrine', 'rate_dopamine', 'rate_dobutamine']].notna().any(axis=1)
mask3 = has_vaso & (sofa_df['cardiovascular'] < 4) & ((sofa_df['rate_dopamine'] > 5).fillna(False) | (sofa_df['rate_norepinephrine'] <= 0.1).fillna(False) | (sofa_df['rate_epinephrine'] <= 0.1).fillna(False))
sofa_df.loc[mask3.fillna(False), 'cardiovascular'] = 3
# Score 2: dopamine >0 or dobutamine >0
mask2 = has_vaso & (sofa_df['cardiovascular'] < 3) & ((sofa_df['rate_dopamine'] > 0).fillna(False) | (sofa_df['rate_dobutamine'] > 0).fillna(False))
sofa_df.loc[mask2.fillna(False), 'cardiovascular'] = 2
# Score 1: MAP < 70
mask1 = (sofa_df['cardiovascular'] < 2) & (sofa_df['map_final'] < 70)
sofa_df.loc[mask1.fillna(False), 'cardiovascular'] = 1

# CNS (GCS)
sofa_df['cns'] = np.where(
    sofa_df['gcs_min'] < 6, 4,
    np.where(
        (sofa_df['gcs_min'] >= 6) & (sofa_df['gcs_min'] <= 9), 3,
        np.where(
            (sofa_df['gcs_min'] >= 10) & (sofa_df['gcs_min'] <= 12), 2,
            np.where(
                (sofa_df['gcs_min'] >= 13) & (sofa_df['gcs_min'] <= 14), 1,
                0
            )
        )
    )
)
sofa_df['cns'] = sofa_df['cns'].fillna(0)

# Renal
sofa_df['renal'] = 0
mask_r4a = sofa_df['creatinine_final'] >= 5.0
mask_r4b = sofa_df['urineoutput'] < 200
sofa_df.loc[(mask_r4a.fillna(False) | mask_r4b.fillna(False)), 'renal'] = 4
mask_r3a = (sofa_df['creatinine_final'] >= 3.5) & (sofa_df['creatinine_final'] < 5.0)
mask_r3b = sofa_df['urineoutput'] < 500
sofa_df.loc[(sofa_df['renal'] < 4) & (mask_r3a.fillna(False) | mask_r3b.fillna(False)), 'renal'] = 3
mask_r2 = (sofa_df['creatinine_final'] >= 2.0) & (sofa_df['creatinine_final'] < 3.5)
sofa_df.loc[(sofa_df['renal'] < 3) & mask_r2.fillna(False), 'renal'] = 2
mask_r1 = (sofa_df['creatinine_final'] >= 1.2) & (sofa_df['creatinine_final'] < 2.0)
sofa_df.loc[(sofa_df['renal'] < 2) & mask_r1.fillna(False), 'renal'] = 1

# Total SOFA
sofa_df['sofa'] = (sofa_df['respiration'] + sofa_df['coagulation'] + sofa_df['liver'] +
                   sofa_df['cardiovascular'] + sofa_df['cns'] + sofa_df['renal'])

# Summary
print(f"\n=== SOFA Summary (N={len(sofa_df)}) ===")
print(f"SOFA: median {sofa_df['sofa'].median():.1f} [IQR {sofa_df['sofa'].quantile(0.25):.0f}-{sofa_df['sofa'].quantile(0.75):.0f}]")
print(f"SOFA: mean {sofa_df['sofa'].mean():.1f} (SD {sofa_df['sofa'].std():.1f})")
print(f"\nComponent scores (mean):")
for c in ['respiration', 'coagulation', 'liver', 'cardiovascular', 'cns', 'renal']:
    print(f"  {c}: {sofa_df[c].mean():.2f}")

# Merge with CC dataset
cc_with_sofa = cc.merge(sofa_df[['stay_id', 'sofa', 'respiration', 'coagulation', 'liver',
                                  'cardiovascular', 'cns', 'renal']], on='stay_id', how='left')

# SOFA by outcome
print(f"\nSOFA by outcome:")
dead = cc_with_sofa[cc_with_sofa['hospital_expire_flag'] == 1]
alive = cc_with_sofa[cc_with_sofa['hospital_expire_flag'] == 0]
print(f"  Died: median {dead['sofa'].median():.1f} [IQR {dead['sofa'].quantile(0.25):.0f}-{dead['sofa'].quantile(0.75):.0f}]")
print(f"  Survived: median {alive['sofa'].median():.1f} [IQR {alive['sofa'].quantile(0.25):.0f}-{alive['sofa'].quantile(0.75):.0f}]")

from scipy.stats import mannwhitneyu
stat, p = mannwhitneyu(dead['sofa'], alive['sofa'])
print(f"  Mann-Whitney U P: {p:.2e}")

# Save
sofa_df[['stay_id', 'sofa', 'respiration', 'coagulation', 'liver', 'cardiovascular', 'cns', 'renal']].to_csv(
    f"{OUTPUT_DIR}/sofa_scores.csv", index=False)
print(f"\nSaved sofa_scores.csv")

# Also save updated CC dataset with SOFA
cc_with_sofa.to_csv(f"{OUTPUT_DIR}/analysis_dataset_with_sofa.csv", index=False)
print(f"Saved analysis_dataset_with_sofa.csv")
