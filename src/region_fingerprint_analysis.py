# src/region_fingerprint_analysis.py

import os
import glob
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from project_paths import COHORTS_DIR, SLICES_DIR, OUTPUTS_DIR

# CONFIG: cohort you're analyzing
cohort_tag = "2014-12_multi"

# Load cohort data to define time window
cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
df = pd.read_csv(cohort_file)
df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y")

# Define cohort date window (+/- buffer)
min_date = df['date'].min() - pd.Timedelta(days=40)
max_date = df['date'].max() + pd.Timedelta(days=7)

# Locate SST slice files
slices_dir = os.path.join(SLICES_DIR, "sst_master_slices")
all_slices = sorted(glob.glob(os.path.join(slices_dir, "sst_celsius_*.nc")))

# Filter files within cohort window
slice_files = [
    f for f in all_slices
    if min_date <= pd.to_datetime(os.path.basename(f).split("_")[-1].split(".nc")[0]) <= max_date
]

# Define regions for analysis
regions = {
    "Bight_Core": {
        "lat_range": slice(32.5, 34.5),
        "lon_range": slice(-121.5, -117.5),
    },
    "Transition_Zone": {
        "lat_range": slice(34.5, 36),
        "lon_range": slice(-122, -119),
    },
    "North_Offshore": {
        "lat_range": slice(36, 50),
        "lon_range": slice(-125, -122),
    }
}

# Prepare regional output storage
region_results = {region: [] for region in regions}

# Loop over all valid files
for file in slice_files:
    ds = xr.open_dataset(file)
    sst_celsius = ds['sst_celsius']
    date_val = pd.to_datetime(str(sst_celsius.time.values)[:10])

    for region, bounds in regions.items():
        try:
            subset = sst_celsius.sel(
                latitude=bounds['lat_range'],
                longitude=bounds['lon_range']
            )
            regional_mean = subset.mean().values.item()
            region_results[region].append({'date': date_val, 'mean_sst_c': regional_mean})
        except Exception as e:
            print(f"⚠️ Skipped file {file} for region {region} due to: {e}")

# Plot everything
fig, axes = plt.subplots(len(regions), 1, figsize=(10, 12), sharex=True)

for i, (region, records) in enumerate(region_results.items()):
    region_df = pd.DataFrame(records).sort_values('date')
    region_df['rolling_mean'] = region_df['mean_sst_c'].rolling(window=7, center=True).mean()
    region_df['anomaly'] = region_df['mean_sst_c'] - region_df['rolling_mean']

    ax = axes[i]
    ax.plot(region_df['date'], region_df['anomaly'], color="purple")
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_ylabel("Anomaly (°C)")
    ax.set_title(f"{region} SST Fingerprint")

    # Annotate with mean SST
    base_temp = region_df['mean_sst_c'].mean()
    legend_label = f"{region} anomaly\nMean SST: {base_temp:.2f}°C"
    ax.legend([legend_label], loc='upper right')

    # Save CSV per region
    out_csv = os.path.join(OUTPUTS_DIR, cohort_tag, f"{region}_sst_anomaly.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    region_df.to_csv(out_csv, index=False)

plt.xlabel("Date")
plt.tight_layout()
out_fig = os.path.join(OUTPUTS_DIR, cohort_tag, f"{cohort_tag}_regional_sst_fingerprint.png")
plt.savefig(out_fig, dpi=150)
plt.show()

print(f"🎯 Full regional analysis complete → {out_fig}")
