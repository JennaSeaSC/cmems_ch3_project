# master_timeseries_sst_abs_val

import os
import glob
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from project_paths import SLICES_DIR, OUTPUTS_DIR

# Input directory where your daily slices live
slices_dir = os.path.join(SLICES_DIR, "sst_master_slices")
slice_files = sorted(glob.glob(os.path.join(slices_dir, "sst_celsius_*.nc")))

# Define regions
regions = {
    "Bight_Core": {"lat_range": slice(32.5, 34.5), "lon_range": slice(-121.5, -117.5)},
    "Transition_Zone": {"lat_range": slice(34.5, 36), "lon_range": slice(-122, -119)},
    "North_Offshore": {"lat_range": slice(36, 46), "lon_range": slice(-125, -122)}
}

# Storage
region_results = {region: [] for region in regions}

# Process each daily slice
for file in slice_files:
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

# Prepare output directory for master fingerprint climatology
fingerprint_out_dir = os.path.join(OUTPUTS_DIR, "regional_climatology")
os.makedirs(fingerprint_out_dir, exist_ok=True)

# === Plot everything ===
fig, axes = plt.subplots(len(regions), 1, figsize=(10, 12), sharex=True)

for i, (region, records) in enumerate(region_results.items()):
    region_df = pd.DataFrame(records).sort_values('date')
    region_df['rolling_mean'] = region_df['mean_sst_c'].rolling(window=7, center=True).mean()
    region_df['anomaly'] = region_df['mean_sst_c'] - region_df['rolling_mean']
    regional_mean_temp = region_df['mean_sst_c'].mean()

    ax = axes[i]
    ax.plot(region_df['date'], region_df['anomaly'], color="purple")
    ax.axhline(0, color='gray', linestyle='--')
    ax.text(region_df['date'].iloc[5], 0.5, f"Mean SST: {regional_mean_temp:.2f}°C", fontsize=10)
    ax.set_ylabel("Anomaly (°C)")
    ax.set_title(f"{region} SST Fingerprint")
    ax.legend([f"{region} anomaly"], loc='upper right')

    # Save per-region CSV
    csv_out = os.path.join(fingerprint_out_dir, f"{region}_sst_anomaly.csv")
    region_df.to_csv(csv_out, index=False)

plt.xlabel("Date")
plt.tight_layout()
plt.savefig(os.path.join(fingerprint_out_dir, "regional_sst_fingerprints.png"), dpi=150)
plt.show()

print("🎯 Full regional climatology fingerprints complete →", fingerprint_out_dir)
