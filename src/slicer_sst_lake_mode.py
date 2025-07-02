# src/slicer_sst_lake_mode.py

import xarray as xr
import os
import numpy as np

# ✅ Hardcoded lake extent — full California Current domain
min_lon, max_lon = -137, -115  
min_lat, max_lat = 31.9, 53

# ✅ Point to lake SST file (already downloaded to your T7)
LAKE_DATA_DIR = "/mnt/e/cmems_data_lake/data"
sst_file = os.path.join(LAKE_DATA_DIR, "sst_master.nc")

# ✅ Output: slices saved directly to your ch3 repo for analysis
OUTPUT_SLICE_DIR = "./slices/sst_master_slices"
os.makedirs(OUTPUT_SLICE_DIR, exist_ok=True)

# ✅ Load entire master SST dataset
ds = xr.open_dataset(sst_file)

# ✅ Extract & convert SST → Celsius
sst_kelvin = ds['analysed_sst']
sst_celsius = sst_kelvin - 273.15

# ✅ Apply full lake spatial mask
sst_celsius = sst_celsius.sel(
    longitude=slice(min_lon, max_lon),
    latitude=slice(min_lat, max_lat)
)

# ✅ Slice temporally and export daily NetCDFs
for t in sst_celsius.time.values:
    date_str = str(t)[:10]
    slice_ds = sst_celsius.sel(time=t)

    # Wrap into Dataset (not just DataArray → better NetCDF output)
    daily_ds = slice_ds.to_dataset(name="sst_celsius")

    out_path = os.path.join(OUTPUT_SLICE_DIR, f"sst_celsius_{date_str}.nc")
    daily_ds.to_netcdf(out_path)
    print(f"✅ Saved slice: {out_path}")
