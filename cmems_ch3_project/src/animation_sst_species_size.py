# render_dynamic_animation.py

import os
import glob
import cmocean
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import imageio.v2 as imageio
from matplotlib.lines import Line2D
from project_paths import COHORTS_DIR, OUTPUTS_DIR, SLICES_DIR

# CONFIG
cohort_tag = "2015-12_multi"
cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
df = pd.read_csv(cohort_file)
df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y")

# Define cohort date window (+/- buffer)
min_date = df['date'].min() - pd.Timedelta(days=40)
max_date = df['date'].max() + pd.Timedelta(days=7)

# Locate all SST NetCDF slices
sst_dir = os.path.join(SLICES_DIR, "sst_master_slices")
sst_files_all = sorted(glob.glob(os.path.join(sst_dir, "sst_celsius_*.nc")))

# Filter SST files to only those within cohort window
sst_files = [
    f for f in sst_files_all 
    if min_date <= pd.to_datetime(os.path.basename(f).split("_")[-1].split(".nc")[0]) <= max_date
]

# Output frame directory
frames_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "frames")
if os.path.exists(frames_dir):
    import shutil
    shutil.rmtree(frames_dir)
os.makedirs(frames_dir, exist_ok=True)

# Define species color mapping
species_colors = {
    "CM": "#355e3b",   # Green turtle → dark olive/green-brown (true to shell + skin)
    "LO": "#a2a660",   # Olive ridley → muted olive yellow-green (shell and name!)
    "CC": "#b05c38"    # Loggerhead → orangey-brown (carapace realness)
}

# Define age-based sizes
size_mapping = {
    "immature": 50,
    "adult": 120
}

# Build frames
for i, sst_file in enumerate(sst_files):
    sst = xr.open_dataset(sst_file)['sst_celsius']
    time_val = pd.to_datetime(str(sst.time.values)[:10])

    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    sst.plot(
        ax=ax,
        cmap='cmo.thermal',
        vmin=8,
        vmax=20,
        transform=ccrs.PlateCarree(),
        cbar_kwargs={'label': 'SST (°C)'}
    )

    ax.coastlines(resolution="10m")
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.gridlines(draw_labels=True, linestyle="--")

    # Cumulative strandings up to this frame date
    stranding_now = df[df['date'] <= time_val]

    # Get visual variables
    colors = stranding_now['species'].map(species_colors).fillna("gray")
    sizes = stranding_now['age_class'].map(size_mapping).fillna(80)

    # Plot strandings
    ax.scatter(
        stranding_now['lon'],
        stranding_now['lat'],
        s=sizes,
        c=colors,
        edgecolors="black",
        transform=ccrs.PlateCarree(),
        zorder=5,
        alpha=0.9
    )

    # === LEGEND FOR SPECIES COLORS ===
    species_legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Green (CM)',
               markerfacecolor="#355e3b", markersize=10, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Olive Ridley (LO)',
               markerfacecolor="#a2a660", markersize=10, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Loggerhead (CC)',
               markerfacecolor="#b05c38", markersize=10, markeredgecolor='black')
    ]

    # === LEGEND FOR AGE CLASSES ===
    age_legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Immature',
               markerfacecolor='gray', markersize=6, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Adult',
               markerfacecolor='gray', markersize=12, markeredgecolor='black')
    ]

    # Add first legend (Species) near upper right
    legend1 = ax.legend(
        handles=species_legend_elements,
        title="Species",
        loc='upper right',
        bbox_to_anchor=(1.0, 1.0),  # top right of axes
        frameon=True
    )

    # Add second legend (Age Class) just below the first
    legend2 = ax.legend(
        handles=age_legend_elements,
        title="Age Class",
        loc='upper right',
        bbox_to_anchor=(1.0, 0.75),  # slightly lower down
        frameon=True
    )

    # Add both
    ax.add_artist(legend1)
    ax.add_artist(legend2)


    # Dynamic title
    ax.set_title(f"Stranding Onset & SST Change — Through {time_val.date()}")

    frame_path = os.path.join(frames_dir, f"{i:03d}.png")
    plt.savefig(frame_path, dpi=150)
    plt.close()

    print(f"✅ Frame {i+1} complete")

# Build final MP4 animation
frames = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
images = [imageio.imread(f) for f in frames]

final_mp4_path = os.path.join(OUTPUTS_DIR, cohort_tag, f"{cohort_tag}_sst_strandings_anim.mp4")
imageio.mimsave(final_mp4_path, images, fps=10)

print("🎯 Final animation saved →", final_mp4_path)
