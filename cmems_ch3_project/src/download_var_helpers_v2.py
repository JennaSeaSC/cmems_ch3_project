# src/download_var_helpers_v2.py

from copernicusmarine import subset

def download_variable(dataset_id, variable_name, time_range, bbox, output_filename):
    """
    Generalized downloader for CMEMS using copernicusmarine Toolbox.
    """
    subset(
        dataset_id=dataset_id,
        variables=variable_name,
        start_datetime=time_range[0],
        end_datetime=time_range[1],
        minimum_longitude=bbox[0],
        maximum_longitude=bbox[1],
        minimum_latitude=bbox[2],
        maximum_latitude=bbox[3],
        output_filename=output_filename,
        overwrite=True
    )

