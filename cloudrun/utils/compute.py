def parse_instance_name(resource_name: str):

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "zone": parts[6],
        "instance": parts[8],
    }