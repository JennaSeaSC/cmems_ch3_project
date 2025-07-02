# src/percentile_analysis.py

import os
import pandas as pd
import numpy as np
import xarray as xr
import glob
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore
from project_paths import SLICES_DIR, COHORTS_DIR, OUTPUTS_DIR

# CONFIG
cohort_tag = "2015-12_multi"

# Load cohort CSV
cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
df = pd.read_csv(cohort_file)
df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y")
buffer_days = 40
min_date = df['date'].min() - pd.Timedelta(days=buffer_days)
max_date = df['date'].max() + pd.Timedelta(days=7)

# Regions (consistent with prior regional slicing)
regions = {
    "Bight_Core":      {"lat_range": slice(32.5, 34.5), "lon_range": slice(-121.5, -117.5)},
    "Transition_Zone": {"lat_range": slice(34.5, 36),   "lon_range": slice(-122, -119)},
    "North_Offshore":  {"lat_range": slice(36, 46),     "lon_range": slice(-125, -122)}
}

# Load all slices for full climatology
slice_dir = os.path.join(SLICES_DIR, "sst_master_slices")
all_slices = sorted(glob.glob(os.path.join(slice_dir, "sst_celsius_*.nc")))

# Build climatology per region
region_climatology = {region: [] for region in regions}

for file in all_slices:
    ds = xr.open_dataset(file)
    sst_c = ds['sst_celsius']
    for region, bounds in regions.items():
        subset = sst_c.sel(latitude=bounds['lat_range'], longitude=bounds['lon_range'])
        mean_val = subset.mean().values.item()
        region_climatology[region].append(mean_val)

# Filter files for cohort window (filename parsing fully synced now!)
cohort_files = [
    f for f in all_slices
    if min_date <= pd.to_datetime(os.path.basename(f).split("_")[-1].split(".nc")[0]) <= max_date
]

# Compute cohort percentiles
region_results = []

for region, bounds in regions.items():
    cohort_ssts = []
    for file in cohort_files:
        ds = xr.open_dataset(file)
        sst_c = ds['sst_celsius']
        subset = sst_c.sel(latitude=bounds['lat_range'], longitude=bounds['lon_range'])
        mean_val = subset.mean().values.item()
        cohort_ssts.append(mean_val)

    if cohort_ssts:
        cohort_mean = np.mean(cohort_ssts)
        percentile = percentileofscore(region_climatology[region], cohort_mean)
        region_results.append({
            'region': region,
            'cohort_mean_sst': cohort_mean,
            'percentile_rank': percentile
        })

# Save output CSV
output_dir = os.path.join(OUTPUTS_DIR, cohort_tag)
os.makedirs(output_dir, exist_ok=True)
results_file = os.path.join(output_dir, f"{cohort_tag}_sst_percentiles.csv")
pd.DataFrame(region_results).to_csv(results_file, index=False)
print(f"✅ Percentile analysis complete → {results_file}")

# === PLOT ===

df_plot = pd.DataFrame(region_results)
plt.figure(figsize=(10, 6))

for i, row in df_plot.iterrows():
    plt.scatter(i, row['cohort_mean_sst'], s=150, color='navy', edgecolor='white', zorder=3)
    plt.text(i, row['cohort_mean_sst'] + 0.15, f"{row['percentile_rank']:.1f}%", 
             ha='center', fontsize=10)

plt.xticks(range(len(df_plot)), df_plot['region'])
plt.ylabel("Cohort Mean SST (°C)")
plt.title(f"Cohort Mean SST & Percentile Ranks: {cohort_tag}")
plt.axhline(y=df_plot['cohort_mean_sst'].mean(), color='gray', linestyle='--', label='Cohort Overall Mean')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.legend()
plt.tight_layout()

fig_out = os.path.join(output_dir, f"{cohort_tag}_sst_percentile_plot.png")
plt.savefig(fig_out, dpi=150)
plt.show()

print(f"🎯 Percentile plot saved → {fig_out}")
