# src/download_helpers.py
def download_variable(dataset_id, variable_name, time_range, bbox, output_filename):    
        # this is the reusable logic flow here
    from copernicusmarine import subset
    subset(
        dataset_id=dataset_id,
        variables=variable_name,
        start_datetime=time_range[0],
        end_datetime=time_range[1],
        minimum_longitude=bbox[0],
        maximum_longitude=bbox[2],
        minimum_latitude=bbox[1],
        maximum_latitude=bbox[3],
        output_filename=f"data/{output_filename}"
    )
    
