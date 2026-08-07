"""
Extract vital signs from MIMIC-IV chartevents for acute abdomen cohort.
Only extracts relevant itemids in chunks to handle the 3.3GB file efficiently.
"""
import pandas as pd, os, sys, gzip

BASE = 'E:/mimic-iv/v3.1/physionet.org/files/mimiciv/3.1'
OUT = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'

# Key itemids for vital signs
VITAL_ITEMIDS = {
    220045: 'Heart_Rate',
    220050: 'SBP_arterial',
    220051: 'DBP_arterial',
    220052: 'MAP_arterial',
    220179: 'SBP_nibp',
    220180: 'DBP_nibp',
    220181: 'MAP_nibp',
    224167: 'SBP_manual_L',
    227243: 'SBP_manual_R',
    224643: 'DBP_manual_L',
    227242: 'DBP_manual_R',
    225309: 'SBP_art_line',
    225310: 'DBP_art_line',
    225312: 'MAP_art_line',
    220210: 'Respiratory_Rate',
    220277: 'SpO2',
    223761: 'Temperature_F',
    223762: 'Temperature_C',
}

itemid_set = set(VITAL_ITEMIDS.keys())

# Load cohort stay_ids (ICU patients have stay_ids)
print('Loading cohort admissions...')
cohort = pd.read_csv(os.path.join(OUT, 'cohort_admissions.csv'))
cohort_hadm = set(cohort['hadm_id'].values)
print(f'Cohort hadm_ids: {len(cohort_hadm)}')

# Load icustays to get stay_ids for our cohort
print('Loading icustays...')
icu = pd.read_csv(os.path.join(BASE, 'icu/icustays.csv.gz'))
icu_cohort = icu[icu['hadm_id'].isin(cohort_hadm)].copy()
cohort_stay_ids = set(icu_cohort['stay_id'].values)
print(f'Cohort ICU stay_ids: {len(cohort_stay_ids)}')

# Also need non-ICU patients - chartevents is only for ICU patients
# For non-ICU ED patients, vital signs come from omr or chartevents during ED stay
# Actually chartevents covers ICU stays only. For ED vitals we need different approach.

# Extract ICU vital signs from chartevents
print('\nExtracting vital signs from chartevents (chunked)...')
chunk_size = 500000
vital_records = []

chartevents_path = os.path.join(BASE, 'icu/chartevents.csv.gz')
reader = pd.read_csv(chartevents_path, chunksize=chunk_size,
                     usecols=['subject_id', 'hadm_id', 'stay_id', 'caregiver_id',
                              'charttime', 'storetime', 'itemid', 'value', 'valuenum'])

total_chunks = 0
matched_chunks = 0
total_records = 0

for chunk in reader:
    total_chunks += 1
    # Filter: cohort patients + vital sign itemids
    mask = (chunk['hadm_id'].isin(cohort_hadm)) & (chunk['itemid'].isin(itemid_set))
    filtered = chunk[mask]

    if len(filtered) > 0:
        matched_chunks += 1
        # Add label column
        filtered['vital_label'] = filtered['itemid'].map(VITAL_ITEMIDS)
        vital_records.append(filtered[['subject_id','hadm_id','stay_id','charttime','itemid','valuenum','vital_label']].copy())
        total_records += len(filtered)

    if total_chunks % 20 == 0:
        print(f'  Chunk {total_chunks}: total_records={total_records}')

    # Early stop if we've processed enough
    if total_chunks > 200:  # Safety limit
        print(f'  Stopping at chunk {total_chunks} for efficiency')
        break

print(f'\nTotal chunks: {total_chunks}, matched: {matched_chunks}')
print(f'Total vital sign records extracted: {total_records}')

# Combine and save
if vital_records:
    vitals = pd.concat(vital_records, ignore_index=True)
    print(f'Combined vitals shape: {vitals.shape}')
    print(f'Vital label distribution:')
    print(vitals['vital_label'].value_counts().to_string())

    vitals.to_csv(os.path.join(OUT, 'icu_vitals.csv'), index=False)
    print(f'Saved ICU vitals to {OUT}/icu_vitals.csv')
else:
    print('No vital records found!')
