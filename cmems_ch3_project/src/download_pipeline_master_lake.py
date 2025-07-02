# src/download_pipeline_master_lake.py

import os
from download_var_helpers_v2 import download_variable

# === MASTER TIME RANGE ===  
# (this is your full historical record — you can modify if you ever extend your dataset)

time_range = ("2009-10-01", "2025-05-14")

# === MASTER BOUNDING BOX ===  
# Big enough to fully encompass your turtles & oceanography
# (California Current + Baja, full corridor of interest)

min_lon, max_lon = -137, -115  
min_lat, max_lat = 31.9, 53
bbox = (min_lon, max_lon, min_lat, max_lat)

# === OUTPUT LOCATION ===
BASE_DIR = "/mnt/e/cmems_data_lake/data"

# SST download
download_variable(
    dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST",
    variable_name=["analysed_sst"],
    time_range=time_range,
    bbox=bbox,
    output_filename=os.path.join(BASE_DIR, "sst_master.nc")
)

# Wind download
download_variable(
    dataset_id="cmems_obs-wind_glo_phy_my_l4_0.125deg_PT1H",
    variable_name=["eastward_wind", "northward_wind"],
    time_range=time_range,
    bbox=bbox,
    output_filename=os.path.join(BASE_DIR, "wind_master.nc")
)

# Wave download
download_variable(
    dataset_id="cci_obs-wave_glo_phy-swh_my_j2-l3_PT1S",
    variable_name=["VAVH"],
    time_range=time_range,
    bbox=bbox,
    output_filename=os.path.join(BASE_DIR, "waves_master.nc")
)

print("🎯 The Big Lake Download COMPLETE")
