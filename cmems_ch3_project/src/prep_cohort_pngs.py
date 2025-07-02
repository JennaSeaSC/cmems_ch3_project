# src/prep_cohort_pngs.py

import os
import glob
import pandas as pd
import shutil
from project_paths import OUTPUTS_DIR, COHORTS_DIR, PNG_DIR

# CONFIG: Name your cohort
cohort_tag = "2015-12_multi"

# Locate cohort CSV and load
cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
df = pd.read_csv(cohort_file)
df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y")

# Determine date window
min_date = df['date'].min() - pd.Timedelta(days=40)
max_date = df['date'].max() + pd.Timedelta(days=7)

# ✅ FULL PNG MASTER LOCATION (hardcoded and stable now)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
full_png_dir = os.path.join(project_root, "outputs", "sst_full_timeseries")
all_pngs = sorted(glob.glob(os.path.join(full_png_dir, "*.png")))

# Build output directory for this cohort
cohort_anim_dir = os.path.join(PNG_DIR, cohort_tag, "animation")
os.makedirs(cohort_anim_dir, exist_ok=True)

# Optional: Clear directory if it already exists
if os.path.exists(cohort_anim_dir):
    shutil.rmtree(cohort_anim_dir)
os.makedirs(cohort_anim_dir, exist_ok=True)

# Filter and copy only matching PNGs for this cohort
count = 0
for png in all_pngs:
    date_str = os.path.basename(png).replace(".png", "")
    file_date = pd.to_datetime(date_str)

    if min_date <= file_date <= max_date:
        dest_path = os.path.join(cohort_anim_dir, os.path.basename(png))
        shutil.copy2(png, dest_path)
        count += 1

print(f"✅ Copied {count} PNGs into {cohort_anim_dir}")
