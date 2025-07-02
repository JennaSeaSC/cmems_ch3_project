# # src/download_helpers.py

# from copernicusmarine import subset

# def download_variable(dataset_id, variable_name, time_range, bbox, output_filename):
#     subset(
#         dataset_id=dataset_id,
#         variables=variable_name,
#         start_datetime=time_range[0],
#         end_datetime=time_range[1],
#         minimum_longitude=bbox[0],
#         maximum_longitude=bbox[2],
#         minimum_latitude=bbox[1],
#         maximum_latitude=bbox[3],
#         output_filename = output_filename,
#         overwrite=True
#     )

# src/download_var_helpers.py

from copernicusmarine import subset
import os

def download_variable(dataset_id, variable_name, time_range, bbox, output_filename, overwrite_existing=True):
    """
    Generic downloader for any Copernicus Marine dataset.
    """
    output_path = os.path.join("data", output_filename)

    # Handle overwrite logic
    if os.path.exists(output_path) and not overwrite_existing:
        print(f"⚠ File already exists: {output_path} — Skipping download.")
        return

    print(f"📥 Downloading: {output_filename}")

    subset(
        dataset_id=dataset_id,
        variables=variable_name,
        start_datetime=time_range[0],
        end_datetime=time_range[1],
        minimum_longitude=bbox[0],
        maximum_longitude=bbox[1],
        minimum_latitude=bbox[2],
        maximum_latitude=bbox[3],
        output_filename=output_path,
        file_format="netcdf"
    )

    print(f"✅ Download complete → {output_path}")

