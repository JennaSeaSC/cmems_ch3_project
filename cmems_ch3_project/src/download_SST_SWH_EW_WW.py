# src/download_variables.py
from download_helpers import download_variable

# Common bounding box and time range
bbox = (-125.85, -124.03, 43.86, 45.02)
time_range = ("2009-10-23", "2009-11-22")

# SST
download_variable(
    dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST", # SST_GLO_SST_L4_REP_OBSERVATIONS_010_011
    variable_name=["analysed_sst"],
    time_range=time_range,
    bbox=bbox,
    output_filename="sst_2009-11-22.nc"
)

# Wind speed
download_variable(
    dataset_id="cmems_obs-wind_glo_phy_my_l4_0.125deg_PT1H", # WIND_GLO_PHY_L4_MY_012_006
    variable_name=["eastward_wind", "northward_wind"],
    time_range=time_range,
    bbox=bbox,
    output_filename="wind_2009-11-22.nc"
)

# Wave height (significant wave height)
download_variable(
    dataset_id="cci_obs-wave_glo_phy-swh_my_j2-l3_PT1S", # WAVE_GLO_PHY_SWH_L3_MY_014_005
    variable_name=["VAVH"],
    time_range=time_range,
    bbox=bbox,
    output_filename="waves_2009-11-22.nc"
)
