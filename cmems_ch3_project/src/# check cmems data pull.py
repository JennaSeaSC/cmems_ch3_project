# check cmems data pull
import xarray as xr
import matplotlib.pyplot as plt

# Load the file
ds = xr.open_dataset("data/sst/sst_stranding_2009-11-22.nc")

# Peek inside
print(ds)
print(ds.variables)

# Optional: plot a snapshot
ds['analysed_sst'].isel(time=0).plot()
