# assign_regions_to_strandings.py

import os
import pandas as pd
import glob

# Path to your cohorts directory
COHORTS_DIR = "/home/jenna/dissertation_chapters/cmems_ch3_project/cohorts"

# Define bounding boxes for regions (adjust as needed)
regions = {
    "Bight_Core": {"lat": (32.5, 34.5), "lon": (-121.5, -117.5)},
    "Transition_Zone": {"lat": (34.5, 36), "lon": (-122, -119)},
    "North_Offshore": {"lat": (36, 50), "lon": (-126, -122)}
}

# Function to assign region
def assign_region(lat, lon):
    for region, bounds in regions.items():
        if bounds["lat"][0] <= lat <= bounds["lat"][1] and bounds["lon"][0] <= lon <= bounds["lon"][1]:
            return region
    return "Unclassified"

# Find all relevant CSVs in cohorts dir
csv_files = sorted(glob.glob(os.path.join(COHORTS_DIR, "*_multi_stranding.csv")))

for csv_path in csv_files:
    df = pd.read_csv(csv_path)

    # Confirm required columns are present
    if not {"lat", "lon"}.issubset(df.columns):
        print(f"⚠️ Skipping {os.path.basename(csv_path)} — missing lat/lon columns.")
        continue

    # Assign region
    df["region"] = df.apply(lambda row: assign_region(row["lat"], row["lon"]), axis=1)

    # Save updated CSV back
    df.to_csv(csv_path, index=False)
    print(f"✅ Updated {os.path.basename(csv_path)} with region assignments")
