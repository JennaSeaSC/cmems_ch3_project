# # src/analyzer_sst_cohort.py

# import os
# import pandas as pd
# import xarray as xr
# import matplotlib.pyplot as plt
# import glob
# from project_paths import SLICES_DIR, COHORTS_DIR, OUTPUTS_DIR

# # --- CONFIG ---
# cohort_tag = "2009-11_multi"
# buffer_days = 40

# # Load cohort CSV
# cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
# df = pd.read_csv(cohort_file)
# df['date'] = pd.to_datetime(df['date'])

# start_date = df['date'].min() - pd.Timedelta(days=buffer_days)
# end_date = df['date'].max() + pd.Timedelta(days=7)

# # Regions you defined:
# regions = {
#     "Bight_Core": {
#         "lat_range": slice(32.5, 34.5),
#         "lon_range": slice(-121.5, -117.5),
#     },
#     "Transition_Zone": {
#         "lat_range": slice(34.5, 36),
#         "lon_range": slice(-122, -119),
#     },
#     "North_Offshore": {
#         "lat_range": slice(36, 46),
#         "lon_range": slice(-125, -122),
#     }
# }

# # Load slice files from correct cohort
# slices_dir = os.path.join(SLICES_DIR, cohort_tag)
# slice_files = sorted(glob.glob(os.path.join(slices_dir, "sst_celsius_*.nc")))

# # Filter to cohort date window
# filtered_files = [
#     f for f in slice_files
#     if start_date <= pd.to_datetime(os.path.basename(f)[12:22]) <= end_date
# ]

# # Prepare region outputs
# region_results = {region: [] for region in regions.keys()}

# for file in filtered_files:
#     ds = xr.open_dataset(file)
#     date = pd.to_datetime(str(ds.time.values)[:10])

#     for region, bounds in regions.items():
#         subset = ds['sst_celsius'].sel(
#             latitude=bounds['lat_range'],
#             longitude=bounds['lon_range']
#         )

#         mean_sst = subset.mean().values
#         region_results[region].append({'date': date, 'mean_sst_c': mean_sst})

# # Plot everything
# fig, axes = plt.subplots(len(regions), 1, figsize=(10, 12), sharex=True)

# for i, (region, records) in enumerate(region_results.items()):
#     region_df = pd.DataFrame(records).sort_values('date')
#     region_df['rolling_mean'] = region_df['mean_sst_c'].rolling(window=7, center=True).mean()
#     region_df['anomaly'] = region_df['mean_sst_c'] - region_df['rolling_mean']

#     # Export CSV
#     region_csv = os.path.join(OUTPUTS_DIR, f"{cohort_tag}_{region}_sst_anomaly.csv")
#     region_df.to_csv(region_csv, index=False)

#     # Plot
#     ax = axes[i]
#     ax.plot(region_df['date'], region_df['anomaly'], label=f"{region} anomaly", color="purple")
#     ax.axhline(0, color='gray', linestyle='--')
#     ax.set_ylabel("Anomaly (°C)")
#     ax.set_title(f"{region} SST Fingerprint")
#     ax.legend(loc='upper right')

# plt.xlabel("Date")
# plt.tight_layout()
# region_plot_path = os.path.join(OUTPUTS_DIR, f"{cohort_tag}_regional_sst_fingerprints.png")
# plt.savefig(region_plot_path, dpi=150)
# plt.show()

# print("🎯 All regional fingerprints generated!")
