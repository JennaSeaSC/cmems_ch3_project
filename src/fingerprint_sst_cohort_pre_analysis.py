# # src/fingerprint_preanalysis.py

# import xarray as xr
# import pandas as pd
# import matplotlib.pyplot as plt
# import glob
# import os
# from project_paths import OUTPUTS_DIR, COHORTS_DIR, SLICES_DIR

# # CONFIG — Choose your cohort
# cohort_tag = "2009-11_multi"
# cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
# df = pd.read_csv(cohort_file)
# df['date'] = pd.to_datetime(df['date'])

# # Build your full date window (buffer applied)
# min_date = df['date'].min() - pd.Timedelta(days=40)
# max_date = df['date'].max() + pd.Timedelta(days=7)

# # Load the sliced SST files
# slice_dir = os.path.join(SLICES_DIR, "sst_master_slices")
# all_slices = sorted(glob.glob(os.path.join(slice_dir, "sst_celsius_*.nc")))

# # Filter only slices within date window
# slices_for_cohort = []
# for f in all_slices:
#     file_date = pd.to_datetime(os.path.basename(f).split("_")[-1].split(".")[0])
#     if min_date <= file_date <= max_date:
#         slices_for_cohort.append(f)

# # Aggregate SST across entire box for these dates
# mean_sst_list = []
# for file in slices_for_cohort:
#     ds = xr.open_dataset(file)
#     mean_sst = ds['sst_celsius'].mean().values
#     date = pd.to_datetime(str(ds.time.values)[:10])
#     mean_sst_list.append({'date': date, 'mean_sst_c': mean_sst})

# # Convert to dataframe
# sst_df = pd.DataFrame(mean_sst_list)
# sst_df.sort_values('date', inplace=True)
# sst_df['rolling_mean'] = sst_df['mean_sst_c'].rolling(window=5, center=True).mean()

# # === Plot ===
# plt.figure(figsize=(10,6))
# plt.plot(sst_df['date'], sst_df['mean_sst_c'], label='Daily Mean SST', color='lightblue')
# plt.plot(sst_df['date'], sst_df['rolling_mean'], label='5-day Rolling Mean', color='blue')
# plt.axhline(sst_df['mean_sst_c'].mean(), color='gray', linestyle='--', label='Window Mean')
# plt.xlabel("Date")
# plt.ylabel("SST (°C)")
# plt.title(f"SST Fingerprint: {cohort_tag}")
# plt.legend()
# plt.grid()

# # Save outputs
# output_dir = os.path.join(OUTPUTS_DIR, cohort_tag)
# os.makedirs(output_dir, exist_ok=True)

# csv_out = os.path.join(output_dir, f"{cohort_tag}_sst_timeseries.csv")
# fig_out = os.path.join(output_dir, f"{cohort_tag}_sst_fingerprint.png")

# sst_df.to_csv(csv_out, index=False)
# plt.savefig(fig_out, dpi=150)
# plt.show()

# print("🎯 SST fingerprint analysis complete.")
# print("✅ CSV:", csv_out)
# print("✅ Plot:", fig_out)
