# # minimalistic download pipeline
# import pandas as pd
# from download_var_helpers import download_variable

# # Set your hardcoded bounding box (bigger southward as you wanted)
# west, east, south, north = -134, -116, 30, 46

# # Full time window manually for now:
# time_range = ("2009-10-01", "2009-12-04")

# # Output file path
# output_filename = "data/sst_2009-11-multi.nc"

# # Download SST
# download_variable(
#     dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST",
#     variable_name=["analysed_sst"],
#     time_range=time_range,
#     bbox=(west, east, south, north),
#     output_filename=output_filename
# )

# print("✅ Download complete!")
