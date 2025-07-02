# src/bounding_box_helpers.py

import pyproj
from shapely.geometry import Point, Polygon
from shapely.ops import transform
import pandas as pd

CMEMS_MIN_LON = -180
CMEMS_MAX_LON = 180
CMEMS_MIN_LAT = -90
CMEMS_MAX_LAT = 90

def generate_asymmetric_bounding_box_from_csv(csv_path,
                                               buffer_north_km=350,
                                               buffer_south_km=950,
                                               buffer_west_km=800,
                                               buffer_east_km=1000):
    df = pd.read_csv(csv_path)
    min_lon = df['lon'].min()
    max_lon = df['lon'].max()
    min_lat = df['lat'].min()
    max_lat = df['lat'].max()

    proj_wgs84 = pyproj.CRS("EPSG:4326")
    proj_meters = pyproj.CRS("EPSG:3857")
    project = pyproj.Transformer.from_crs(proj_wgs84, proj_meters, always_xy=True).transform
    reproject = pyproj.Transformer.from_crs(proj_meters, proj_wgs84, always_xy=True).transform

    minx, miny = project(min_lon, min_lat)
    maxx, maxy = project(max_lon, max_lat)

    minx -= buffer_west_km * 1000
    maxx += buffer_east_km * 1000
    miny -= buffer_south_km * 1000
    maxy += buffer_north_km * 1000

    west, south = reproject(minx, miny)
    east, north = reproject(maxx, maxy)

    west = max(west, CMEMS_MIN_LON)
    east = min(east, CMEMS_MAX_LON)
    south = max(south, CMEMS_MIN_LAT)
    north = min(north, CMEMS_MAX_LAT)

    return (west, east, south, north)
