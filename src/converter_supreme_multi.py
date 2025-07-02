# src/converter_supreme_multi.py

import os
import glob
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
from bounding_box_helpers import generate_asymmetric_bounding_box_from_csv

# User inputs
cohort_csv = "cohorts/2009-11_multi_stranding.csv"

# Auto-extract output tag from file name:
output_tag = "2009-11-multi"

# Load cohort
df = pd.read_csv(cohort_csv)

# Bounding box from cohort turtles
west, east, south, north = generate_asymmetric_bounding_box_from_csv(cohort_csv)

# Find slices directory automatically
slices_dir = f"data/slices_{output_tag}"

# Output directory for PNG frames
png_dir = f"png_frames/{output_tag}"
os.makedirs(png_dir, exist_ok=True)

# Process all slice files
nc_files = sorted(glob.glob(os.path.join(slices_dir, 'sst_*.nc')))

for nc_file in nc_files:
    filename = os.path.basename(nc_file)
    date_str = filename.replace('sst_', '').replace('.nc', '')

    ds = xr.open_dataset(nc_file)
    sst = ds['analysed_sst']
    sst_sub = sst.sel(latitude=slice(south, north), longitude=slice(west, east))
    sst_sub = sst_sub.where(sst_sub > 0)

    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # SST plot
    sst_sub.plot(
        ax=ax,
        cmap=cmocean.cm.thermal,
        vmin=8, vmax=20,
        add_colorbar=True,
        cbar_kwargs={'label': 'SST (°C)'}
    )

    ax.coastlines(resolution='10m', linewidth=0.8)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.set_extent([west, east, south, north])

    gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                      linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}

    # Plot strandings up to current date
    cohort_today = df[df['date'] <= date_str]
    for _, row in cohort_today.iterrows():
        ax.plot(row['lon'], row['lat'], marker='o', markersize=36, color='purple',
                markeredgecolor='black', transform=ccrs.PlateCarree(), zorder=5)

    plt.title(f"SST + Strandings on {date_str}", fontsize=14)
    plt.savefig(os.path.join(png_dir, f"{date_str}.png"), dpi=150, bbox_inches='tight', pad_inches=0.05)
    plt.close()

    print(f"✅ Frame {date_str} complete.")

print("🎯 Frame generation complete!")
