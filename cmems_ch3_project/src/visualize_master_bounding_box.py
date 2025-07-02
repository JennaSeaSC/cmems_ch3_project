# src/visualize_master_bounding_box.py

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Use your most up-to-date bounding box (from previous cohort work)
min_lon, max_lon = -137, -115  
min_lat, max_lat = 31.9, 53      

plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.set_extent([min_lon-5, max_lon+5, min_lat-5, max_lat+5], crs=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.BORDERS)
ax.gridlines(draw_labels=True, linestyle='--')

# draw bounding box
plt.plot(
    [min_lon, max_lon, max_lon, min_lon, min_lon],
    [min_lat, min_lat, max_lat, max_lat, min_lat],
    color='red', linewidth=2, transform=ccrs.PlateCarree()
)

plt.title("Proposed CMEMS Data Lake Bounding Box")
plt.show()
