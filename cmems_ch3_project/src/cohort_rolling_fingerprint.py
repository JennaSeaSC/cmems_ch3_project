# src/cohort_rolling_fingerprint.py

import os
import glob
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from project_paths import SLICES_DIR, COHORTS_DIR, OUTPUTS_DIR

# CONFIG
cohort_tag = "2014-12_multi"
buffer_days = 40

# Load cohort CSV
cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
df = pd.read_csv(cohort_file)
df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y")


min_date = df['date'].min() - pd.Timedelta(days=buffer_days)
max_date = df['date'].max() + pd.Timedelta(days=7)

slices_dir = os.path.join(SLICES_DIR, "sst_master_slices")
all_slices = sorted(glob.glob(os.path.join(slices_dir, "sst_celsius_*.nc")))

cohort_files = [
    f for f in all_slices
    if min_date <= pd.to_datetime(os.path.basename(f).split("_")[-1].split(".nc")[0]) <= max_date
]

regions = {
    "Bight_Core": {"lat_range": slice(32.5, 34.5), "lon_range": slice(-121.5, -117.5)},
    "Transition_Zone": {"lat_range": slice(34.5, 36), "lon_range": slice(-122, -119)},
    "North_Offshore": {"lat_range": slice(36, 50), "lon_range": slice(-125, -122)}
}

for region_name, bounds in regions.items():

    records = []
    for file in cohort_files:
        ds = xr.open_dataset(file)
        sst_celsius = ds['sst_celsius']
        date_val = pd.to_datetime(str(sst_celsius.time.values)[:10])

        regional_sst = sst_celsius.sel(
            latitude=bounds["lat_range"],
            longitude=bounds["lon_range"]
        ).mean().values.item()

        records.append({"date": date_val, "mean_sst_c": regional_sst})

    region_df = pd.DataFrame(records).sort_values("date")
    region_df["rolling_mean"] = region_df["mean_sst_c"].rolling(window=5, center=True).mean()

    out_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_rolling_fingerprint")
    os.makedirs(out_dir, exist_ok=True)

    data_out = os.path.join(out_dir, f"{cohort_tag}_{region_name}_rolling_fingerprint.csv")
    region_df.to_csv(data_out, index=False)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(region_df["date"], region_df["mean_sst_c"], color="skyblue", label="Daily Mean SST")
    plt.plot(region_df["date"], region_df["rolling_mean"], color="blue", label="5-day Rolling Mean")
    plt.axhline(region_df["mean_sst_c"].mean(), color="gray", linestyle="--", label="Window Mean")

    plt.title(f"SST Fingerprint: {cohort_tag} ({region_name})")
    plt.ylabel("SST (°C)")
    plt.xlabel("Date")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plot_out = os.path.join(out_dir, f"{cohort_tag}_{region_name}_rolling_fingerprint.png")
    plt.savefig(plot_out, dpi=150)
    plt.show()
    plt.close()

    print(f"🎯 Finished region: {region_name}")
