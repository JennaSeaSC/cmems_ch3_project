# # src/slice_sst_to_images.py

# import xarray as xr
# import os

# # Get most recent SST file downloaded (from download_pipeline.py)
# # You can also directly point if you're testing:
# sst_file = sorted([f for f in os.listdir("data/") if f.startswith("sst_")])[-1]

# # Extract run tag automatically:
# run_tag = sst_file.replace("sst_", "").replace(".nc", "")
# output_dir = f"data/slices_{run_tag}"
# os.makedirs(output_dir, exist_ok=True)

# # Load full NetCDF file
# ds = xr.open_dataset(f"data/{sst_file}")
# sst = ds['analysed_sst']
# sst_celsius = sst - 273.15

# # Loop through each time slice
# for i, t in enumerate(sst_celsius.time.values):
#     date_str = str(t)[:10]
#     slice_ds = sst_celsius.sel(time=t)
#     slice_ds.to_netcdf(f"{output_dir}/sst_{date_str}.nc")
#     print(f"✅ Saved {date_str}")

# print("🎯 All slices complete!")

# src/slice_sst_to_images.py

import xarray as xr
import os
import glob

# Automatically find latest SST file
sst_files = sorted(glob.glob("data/sst_*.nc"))
if not sst_files:
    raise FileNotFoundError("No SST files found in /data/ directory.")
sst_file = sst_files[-1]

# Extract tag for folder naming (remove full path, keep core tag)
tag = os.path.basename(sst_file).replace("sst_", "").replace(".nc", "")
output_dir = f"data/slices_{tag}"
os.makedirs(output_dir, exist_ok=True)

print(f"🔪 Slicing: {sst_file} → {output_dir}/")

# Load dataset
ds = xr.open_dataset(sst_file)
sst = ds['analysed_sst']
sst_celsius = sst - 273.15

# Loop through all time slices
for t in sst_celsius.time.values:
    date_str = str(t)[:10]
    slice_ds = sst_celsius.sel(time=t)
    slice_ds.to_netcdf(f"{output_dir}/sst_{date_str}.nc")
    print(f"✅ Saved slice for {date_str}")

print("🎯 All slicing complete!")
