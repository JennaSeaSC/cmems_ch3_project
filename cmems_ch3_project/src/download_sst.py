# src/download_sst.py
import sys
import copernicusmarine
copernicusmarine.describe("METOFFICE-GLO-SST-L4-REP-OBS-SST")

# === Define SST subset query parameters ===
copernicusmarine.subset(
  dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST",
  variables=["analysed_sst"],
  minimum_longitude=-125.85013056823904,
  maximum_longitude=-124.0265505414764,
  minimum_latitude=43.86791088300122,
  maximum_latitude=45.022242486335735,
  start_datetime="2009-10-23",
  end_datetime="2009-11-22",
  minimum_depth=0,
  maximum_depth=1,
  output_filename = "sst_stranding_2009-11-22.nc",
  output_directory = "data/sst/",
  file_format="netcdf"
)


