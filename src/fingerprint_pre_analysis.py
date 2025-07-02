# # fingerprint_preanalysis.py
# import xarray as xr
# import pandas as pd
# import matplotlib.pyplot as plt

# # Load your full SST dataset
# ds = xr.open_dataset("../data/sst_2009-12-04.nc")

# # Convert SST to Celsius
# sst_celsius = ds['analysed_sst'] - 273.15

# # Spatial average: full bbox avg per time slice
# sst_mean = sst_celsius.mean(dim=["latitude", "longitude"])

# # Convert to Pandas for easy manipulation
# sst_df = sst_mean.to_dataframe().reset_index()
# sst_df['rolling_mean'] = sst_df['analysed_sst'].rolling(window=5, center=True).mean()

# # Plot SST with rolling mean
# plt.figure(figsize=(10,6))
# plt.plot(sst_df['time'], sst_df['analysed_sst'], label='Daily Mean SST', color='lightblue')
# plt.plot(sst_df['time'], sst_df['rolling_mean'], label='5-day Rolling Mean', color='blue')
# plt.axhline(sst_df['analysed_sst'].mean(), color='gray', linestyle='--', label='Window Mean')
# plt.xlabel("Date")
# plt.ylabel("SST (°C)")
# plt.title("SST Fingerprint 2009-11-22 Stranding Window")
# plt.legend()
# plt.grid()
# plt.show()
