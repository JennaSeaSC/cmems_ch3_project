# Average for SST, SWH (NAVH) and EW and NW Wind
import xarray as xr
import pandas as pd
from pathlib import Path

# data oath
data_dir = Path("data")

# Load to get averages
# SST
sst_path = data_dir / "sst_2009-11-22.nc"
sst_ds = xr.open_dataset(sst_path)
sst_var = list(sst_ds.data_vars)[0]  # assuming only one variable
sst_avg = sst_ds[sst_var].mean().item()

# Wind
wind_path = data_dir / "wind_2009-11-22.nc"
wind_ds = xr.open_dataset(wind_path)
wind_var = list(wind_ds.data_vars)[0]
wind_avg = wind_ds[wind_var].mean().item()

# Waves (CSV format)
waves_csv_path = data_dir / "waves_2009-11-22.nc.csv"
waves_df = pd.read_csv(waves_csv_path)
waves_var = "VAVH" if "VAVH" in waves_df.columns else waves_df.columns[-1]
waves_avg = waves_df[waves_var].mean()

# save to summary table
summary = pd.DataFrame({
    "Variable": ["SST", "Wind", "Waves"],
    "Date": ["2009-11-22"] * 3,
    "MeanValue": [sst_avg, wind_avg, waves_avg]
})

summary.to_csv("2009-11-22_averaged_environmental_variables.csv", index=False)
summary
