# src/project_paths.py

import os

# Path to T7 "lake" external drive:
LAKE_DATA_DIR = "/mnt/e/cmems_data_lake/data"

# Path to your repository (repo-managed outputs)
REPO_BASE = os.path.dirname(__file__)  # points to src/

# Subdirectories inside your repo:
SLICES_DIR = os.path.join(REPO_BASE, "../slices")
CONVERTED_DIR = os.path.join(REPO_BASE, "../converted")
OUTPUTS_DIR = os.path.join(REPO_BASE, "../outputs")
COHORTS_DIR = os.path.join(REPO_BASE, "../cohorts")
PNG_DIR = os.path.join(REPO_BASE, "../png_frames")