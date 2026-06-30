def parse_dataset_name(resource_name: str):

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "dataset": parts[6],
    }