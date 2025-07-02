# src/download_pipeline_multivariable.py

import pandas as pd
from download_var_helpers_v2 import download_variable
from bounding_box_helpers import generate_asymmetric_bounding_box_from_csv
from project_paths import DATA_DIR, COHORTS_DIR
import os

# Load cohort CSV (example cohort file here)
cohort_tag = "2009-11_multi"
cohort_csv = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
turtle_df = pd.read_csv(cohort_csv)

min_date = pd.to_datetime(turtle_df['date']).min()
max_date = pd.to_datetime(turtle_df['date']).max()

start_date = (min_date - pd.Timedelta(days=40)).strftime("%Y-%m-%d")
end_date   = (max_date + pd.Timedelta(days=7)).strftime("%Y-%m-%d")
time_range = (start_date, end_date)

print(f"📅 Download window: {time_range}")

bbox = generate_asymmetric_bounding_box_from_csv(cohort_csv)
min_lon, max_lon, min_lat, max_lat = bbox

# SST
download_variable(
    dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST",
    variable_name=["analysed_sst"],
    time_range=time_range,
    bbox=(min_lon, max_lon, min_lat, max_lat),
    output_filename=os.path.join(DATA_DIR, f"sst_{cohort_tag}.nc")
)

# Wind
download_variable(
    dataset_id="cmems_obs-wind_glo_phy_my_l4_0.125deg_PT1H",
    variable_name=["eastward_wind", "northward_wind"],
    time_range=time_range,
    bbox=(min_lon, max_lon, min_lat, max_lat),
    output_filename=os.path.join(DATA_DIR, f"wind_{cohort_tag}.nc")
)

# Waves
download_variable(
    dataset_id="cci_obs-wave_glo_phy-swh_my_j2-l3_PT1S",
    variable_name=["VAVH"],
    time_range=time_range,
    bbox=(min_lon, max_lon, min_lat, max_lat),
    output_filename=os.path.join(DATA_DIR, f"waves_{cohort_tag}.nc")
)

print("🎯 All multivariate downloads complete!")
