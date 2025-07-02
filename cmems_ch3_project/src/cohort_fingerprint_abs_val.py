# src/cohort_fingerprint_absolute.py

import os
import glob
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from project_paths import SLICES_DIR, COHORTS_DIR, OUTPUTS_DIR

# CONFIG
cohort_tag = "2014-12_multi"
buffer_days = 40

# Load cohort CSV
cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
df = pd.read_csv(cohort_file)
df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y")

# Define cohort window
min_date = df['date'].min() - pd.Timedelta(days=buffer_days)
max_date = df['date'].max() + pd.Timedelta(days=7)

# Locate SST slices
slices_dir = os.path.join(SLICES_DIR, "sst_master_slices")
all_slices = sorted(glob.glob(os.path.join(slices_dir, "sst_celsius_*.nc")))

# Filter files to cohort window
cohort_files = [
    f for f in all_slices
    if min_date <= pd.to_datetime(os.path.basename(f).split("_")[-1].split(".nc")[0]) <= max_date
]

# Define regions
regions = {
    "Bight_Core": {"lat_range": slice(32.5, 34.5), "lon_range": slice(-121.5, -117.5)},
    "Transition_Zone": {"lat_range": slice(34.5, 36), "lon_range": slice(-122, -119)},
    "North_Offshore": {"lat_range": slice(36, 50), "lon_range": slice(-125, -122)}
}

# Storage
region_results = {region: [] for region in regions}

# Process cohort slice files
for file in cohort_files:
    ds = xr.open_dataset(file)
    sst_celsius = ds['sst_celsius']
    date_val = pd.to_datetime(str(sst_celsius.time.values)[:10])

    for region, bounds in regions.items():
        regional_sst = sst_celsius.sel(
            latitude=bounds["lat_range"],
            longitude=bounds["lon_range"]
        ).mean().values.item()

        region_results[region].append({
            "date": date_val,
            "mean_sst_c": regional_sst
        })

# Output directory (within cohort folder)
fingerprint_out_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_absolute_fingerprint")
os.makedirs(fingerprint_out_dir, exist_ok=True)

# === Plot everything ===
fig, axes = plt.subplots(len(regions), 1, figsize=(10, 12), sharex=True)

for i, (region, records) in enumerate(region_results.items()):
    region_df = pd.DataFrame(records).sort_values('date')
    regional_mean_temp = region_df['mean_sst_c'].mean()

    ax = axes[i]
    ax.plot(region_df['date'], region_df['mean_sst_c'], color="purple")
    ax.axhline(regional_mean_temp, color='gray', linestyle='--')
    
    # NICE CONSISTENT MEAN SST LABEL POSITION
    ax.text(
        0.98, 0.88, 
        f"Mean SST: {regional_mean_temp:.2f}°C", 
        transform=ax.transAxes, 
        fontsize=10, 
        ha='right', 
        va='top',
        bbox=dict(facecolor='white', alpha=0.6, edgecolor='none')
    )

    ax.set_ylabel("SST (°C)")
    ax.set_title(f"{region} SST Fingerprint")
    ax.legend([f"{region} absolute"], loc='upper right')

    # Save per-region CSV
    csv_out = os.path.join(fingerprint_out_dir, f"{region}_cohort_sst.csv")
    region_df.to_csv(csv_out, index=False)

plt.xlabel("Date")
plt.tight_layout()
plt.savefig(os.path.join(fingerprint_out_dir, f"{cohort_tag}_absolute_sst_fingerprint.png"), dpi=150)
plt.show()

print(f"🎯 Cohort fingerprint complete → {fingerprint_out_dir}")
