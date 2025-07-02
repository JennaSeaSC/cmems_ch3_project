# src/slice_to_images_multivar_t7.py

import xarray as xr
import os
import glob
from project_paths import DATA_DIR, SLICES_DIR

# --- COHORT TAG ---
cohort_tag = "2009-11_multi"

input_dir = os.path.join(DATA_DIR, f"{cohort_tag}")
output_dir = os.path.join(SLICES_DIR, f"{cohort_tag}")
os.makedirs(output_dir, exist_ok=True)

# Supported variables
variable_mappings = {
    "analysed_sst": {"name": "sst_celsius", "offset": -273.15},
    "eastward_wind": {"name": "eastward_wind", "offset": 0},
    "northward_wind": {"name": "northward_wind", "offset": 0},
    "VAVH": {"name": "wave_height", "offset": 0},
}

# Gather all downloaded cohort files
data_files = sorted(glob.glob(f"{input_dir}/*.nc"))
if not data_files:
    raise FileNotFoundError("❌ No NetCDF files found for cohort slicing!")

for data_file in data_files:
    base_file = os.path.basename(data_file).replace(".nc", "")
    ds = xr.open_dataset(data_file)

    for var in ds.data_vars:
        if var not in variable_mappings:
            print(f"⚠️ Skipping unsupported variable: {var}")
            continue

        offset = variable_mappings[var]["offset"]
        sliced_var = ds[var] + offset
        sliced_var = sliced_var.rename(variable_mappings[var]["name"])

        for t in sliced_var.time.values:
            date_str = str(t)[:10]
            slice_ds = sliced_var.sel(time=t)
            slice_ds.to_netcdf(f"{output_dir}/{variable_mappings[var]['name']}_{date_str}.nc")

        print(f"✅ Finished slicing {var} from {base_file}")

print("🎯 All slicing complete for cohort:", cohort_tag)
