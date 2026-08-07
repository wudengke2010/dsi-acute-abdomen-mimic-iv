"""
Efficient full extraction of vital signs from chartevents for ICU acute abdomen cohort.
Processes all chunks without limit.
"""
import pandas as pd, os, sys

BASE = 'E:/mimic-iv/v3.1/physionet.org/files/mimiciv/3.1'
OUT = 'C:/Users/admin/WorkBuddy/2026-07-07-20-09-20/shock_index_abdomen'

# Key itemids only
VITAL_ITEMIDS = {
    220045: 'Heart_Rate',
    220050: 'SBP_arterial',
    220051: 'DBP_arterial',
    220052: 'MAP_arterial',
    220179: 'SBP_nibp',
    220180: 'DBP_nibp',
    220181: 'MAP_nibp',
    220210: 'Respiratory_Rate',
    220277: 'SpO2',
}

itemid_set = set(VITAL_ITEMIDS.keys())

# Load ICU stay_ids for our cohort
icu = pd.read_csv(os.path.join(BASE, 'icu/icustays.csv.gz'))
cohort = pd.read_csv(os.path.join(OUT, 'cohort_admissions.csv'))
icu_cohort = icu[icu['hadm_id'].isin(set(cohort['hadm_id']))]
cohort_stay_ids = set(icu_cohort['stay_id'].values)
print(f'Cohort ICU stay_ids: {len(cohort_stay_ids)}')

# Full extraction with no chunk limit
print('Extracting vital signs from chartevents (full extraction)...')
chunk_size = 1000000  # larger chunks for efficiency
vital_records = []

chartevents_path = os.path.join(BASE, 'icu/chartevents.csv.gz')
reader = pd.read_csv(chartevents_path, chunksize=chunk_size,
                     usecols=['subject_id', 'hadm_id', 'stay_id', 'charttime', 'itemid', 'valuenum'])

total_chunks = 0
total_records = 0

for chunk in reader:
    total_chunks += 1
    # Filter: cohort stay_ids + vital sign itemids
    mask = (chunk['stay_id'].isin(cohort_stay_ids)) & (chunk['itemid'].isin(itemid_set))
    filtered = chunk[mask]

    if len(filtered) > 0:
        filtered = filtered.copy()
        filtered['vital_label'] = filtered['itemid'].map(VITAL_ITEMIDS)
        vital_records.append(filtered[['subject_id','hadm_id','stay_id','charttime','itemid','valuenum','vital_label']])
        total_records += len(filtered)

    if total_chunks % 5 == 0:
        print(f'  Chunk {total_chunks}: total_records={total_records}')

print(f'\nTotal chunks processed: {total_chunks}')
print(f'Total vital sign records: {total_records}')

if vital_records:
    vitals = pd.concat(vital_records, ignore_index=True)
    print(f'\nVital label distribution:')
    print(vitals['vital_label'].value_counts().to_string())
    print(f'\nUnique stays with vitals: {vitals["stay_id"].nunique()}')

    vitals.to_csv(os.path.join(OUT, 'icu_vitals_full.csv'), index=False)
    print(f'Saved to {OUT}/icu_vitals_full.csv')
else:
    print('No vital records found!')
