# src/download_pipeline.py

import pandas as pd
from download_var_helpers import download_variable
from bounding_box_helpers import generate_asymmetric_bounding_box_from_csv

# === USER CONFIG ===

# Path to your multi-turtle CSV file:
MULTI_TURTLE_FILE = "cohorts/2009-11_multi_stranding.csv"

# Load cohort CSV
turtle_df = pd.read_csv(MULTI_TURTLE_FILE)

# Auto-detect min/max dates:
min_date = pd.to_datetime(turtle_df['date']).min()
max_date = pd.to_datetime(turtle_df['date']).max()

# Apply buffer window
from datetime import timedelta
start_date = (min_date - timedelta(days=40)).strftime("%Y-%m-%d")
end_date   = (max_date + timedelta(days=7)).strftime("%Y-%m-%d")
time_range = (start_date, end_date)

print(f"📅 Download window: {time_range}")

# Compute bounding box from CSV
west, east, south, north = generate_asymmetric_bounding_box_from_csv(MULTI_TURTLE_FILE)

# Run Copernicus Marine download:
download_variable(
    dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST",
    variable_name=["analysed_sst"],
    time_range=time_range,
    bbox=(west, east, south, north),
    output_filename=f"data/sst_{end_date}.nc"
)

print("✅ Download complete!")
