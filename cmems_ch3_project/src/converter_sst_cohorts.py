# src/converter_sst_cohort.py

import os
import glob
import pandas as pd
import xarray as xr
from datetime import timedelta

# SETTINGS:
cohort_tag = "2009-11_multi"
BUFFER_DAYS_BEFORE = 40
BUFFER_DAYS_AFTER = 7

# Paths relative to repo root:
base_dir = os.path.dirname(__file__)
slices_dir = os.path.join(base_dir, "../slices/sst_master_slices")
cohorts_dir = os.path.join(base_dir, "../cohorts")
outputs_dir = os.path.join(base_dir, "../outputs", cohort_tag)
os.makedirs(outputs_dir, exist_ok=True)

# Load cohort CSV
cohort_df = pd.read_csv(os.path.join(cohorts_dir, f"{cohort_tag}_stranding.csv"))
cohort_df['date'] = pd.to_datetime(cohort_df['date'])
start_date = cohort_df['date'].min() - timedelta(days=BUFFER_DAYS_BEFORE)
end_date = cohort_df['date'].max() + timedelta(days=BUFFER_DAYS_AFTER)

# Convert SST slices:
sst_files = sorted(glob.glob(f"{slices_dir}/sst_celsius_*.nc"))
results = []

for file in sst_files:
    date_str = os.path.basename(file).split("_")[-1].split(".")[0]
    date_obj = pd.to_datetime(date_str)

    if start_date <= date_obj <= end_date:
        ds = xr.open_dataset(file)
        mean_sst = ds['sst_celsius'].mean().values
        results.append({'date': date_obj, 'sst_celsius': mean_sst})

sst_df = pd.DataFrame(results)
sst_df.to_csv(os.path.join(outputs_dir, f"{cohort_tag}_sst.csv"), index=False)

print("✅ SST conversion complete.")
