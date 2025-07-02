# src/animator_multivar.py

import glob
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import imageio
import os
from pipeline_config import COHORT_TAG

cohort_csv = f"cohorts/{COHORT_TAG}_stranding.csv"
df = pd.read_csv(cohort_csv)

output_dir = f"png_frames_{COHORT_TAG}"
os.makedirs(output_dir, exist_ok=True)

sst_files = sorted(glob.glob(f"data/slices_{COHORT_TAG}/sst_celsius_*.nc"))
wind_files = sorted(glob.glob(f"data/slices_{COHORT_TAG}/eastward_wind_*.nc"))
wave_files = sorted(glob.glob(f"data/slices_{COHORT_TAG}/wave_height_*.nc"))

for i in range(len(sst_files)):
    sst = xr.open_dataset(sst_files[i])['sst_celsius']
    time_val = pd.to_datetime(str(sst.time.values)[:10])

    uwind = xr.open_dataset(wind_files[i])['eastward_wind']
    vwind = xr.open_dataset(wind_files[i].replace("eastward_wind_", "northward_wind_"))['northward_wind']
    waves = xr.open_dataset(wave_files[i])['wave_height']

    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    sst.plot(ax=ax, cmap='cmo.thermal', vmin=8, vmax=20, transform=ccrs.PlateCarree(), cbar_kwargs={'label': 'SST (°C)'})
    waves.plot.contourf(ax=ax, levels=10, alpha=0.3, cmap='Blues', transform=ccrs.PlateCarree())

    skip = (slice(None, None, 5), slice(None, None, 5))
    ax.quiver(uwind.longitude[skip[1]], uwind.latitude[skip[0]],
              uwind.values[skip], vwind.values[skip],
              scale=50, color="black", transform=ccrs.PlateCarree())

    ax.coastlines(resolution="10m")
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.gridlines(draw_labels=True, linestyle="--")

    stranding_now = df[df['date'] <= time_val.strftime("%Y-%m-%d")]
    ax.scatter(stranding_now['lon'], stranding_now['lat'], s=100, c="purple", edgecolors="black", transform=ccrs.PlateCarree(), zorder=5)

    ax.set_title(f"SST + Wind + Waves + Strandings on {time_val.date()}")
    plt.savefig(f"{output_dir}/{i:03d}.png", dpi=150)
    plt.close()

    print(f"✅ Frame {i+1} complete")

frames = sorted(glob.glob(f"{output_dir}/*.png"))
images = [imageio.imread(f) for f in frames]
imageio.mimsave(f"{COHORT_TAG}_multi_variable_animation.mp4", images, fps=10)

print("🎯 MULTI-VARIABLE ANIMATION COMPLETE!")
