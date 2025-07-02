# import xarray as xr
# import os

# # Load full SST file
# sst_file = "data/sst_2009-11-multi.nc"
# output_dir = "data/slices_2009-11-multi"
# os.makedirs(output_dir, exist_ok=True)

# ds = xr.open_dataset(sst_file)
# sst = ds['analysed_sst']
# sst_celsius = sst - 273.15

# for t in sst_celsius.time.values:
#     date_str = str(t)[:10]
#     slice_ds = sst_celsius.sel(time=t)
#     slice_ds.to_netcdf(f"{output_dir}/sst_{date_str}.nc")
#     print(f"✅ Saved {date_str}")
