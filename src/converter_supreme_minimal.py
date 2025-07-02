# import os, glob, xarray as xr, pandas as pd
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs, cartopy.feature as cfeature
# import cmocean

# # Bounding box (same as download)
# west, east, south, north = -134, -116, 30, 46

# # Load your CSV cohort
# turtle_df = pd.read_csv("cohorts/2009-11_multi_stranding.csv")

# # Directories
# input_dir = "data/slices_2009-11-multi"
# output_dir = "png_frames/2009-11-multi"
# os.makedirs(output_dir, exist_ok=True)

# nc_files = sorted(glob.glob(os.path.join(input_dir, "sst_*.nc")))

# for nc_file in nc_files:
#     date_str = os.path.basename(nc_file).replace("sst_", "").replace(".nc", "")
#     ds = xr.open_dataset(nc_file)
#     sst = ds['analysed_sst']
#     sst_sub = sst.sel(latitude=slice(south, north), longitude=slice(west, east)).where(sst > 0)

#     plt.figure(figsize=(10, 8))
#     ax = plt.axes(projection=ccrs.PlateCarree())

#     sst_sub.plot(ax=ax, cmap=cmocean.cm.thermal, vmin=8, vmax=20, add_colorbar=True, cbar_kwargs={'label': 'SST (°C)'})
#     ax.coastlines(resolution='10m', linewidth=0.8)
#     ax.add_feature(cfeature.LAND, facecolor='lightgray')
#     ax.set_extent([west, east, south, north])

#     gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
#     gl.top_labels = False
#     gl.right_labels = False
#     gl.xlabel_style = {'size': 10}
#     gl.ylabel_style = {'size': 10}

#     # Plot turtles appearing cumulatively by date:
#     visible = turtle_df[pd.to_datetime(turtle_df['date']) <= date_str]
#     for _, row in visible.iterrows():
#         ax.plot(row['lon'], row['lat'], marker='o', markersize=30, color='purple', markeredgecolor='black', transform=ccrs.PlateCarree())

#     plt.title(f"SST + Strandings on {date_str}", fontsize=14)
#     plt.savefig(os.path.join(output_dir, f"{date_str}.png"), dpi=150, bbox_inches='tight', pad_inches=0.05)
#     plt.close()

#     print(f"✅ Saved {date_str}")
