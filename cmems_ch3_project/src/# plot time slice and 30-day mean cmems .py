# plot time slice and 30-day mean cmems data pull (sst)
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("data/sst/sst_stranding_2009-11-22.nc")
ds['analysed_sst'].isel(time=0).plot()  # First day
ds['analysed_sst'].mean(dim='time').plot()  # 30-day average

# Peek inside
print(ds)
print(ds.variables)