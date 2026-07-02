def parse_instance_name(resource_name: str):
    """Parses a GCE instance resource name."""
    # Expected format: //compute.googleapis.com/projects/<project>/zones/<zone>/instances/<instance>
    parts = resource_name.split("/")
    return {
        "project": parts[4],
        "zone": parts[6],
        "instance": parts[8],
    }

def parse_disk_name(resource_name: str):
    """Parses a GCE disk resource name."""
    # Expected format: //compute.googleapis.com/projects/<project>/zones/<zone>/disks/<disk>
    parts = resource_name.split("/")
    return {
        "project": parts[4],
        "zone": parts[6],
        "disk": parts[8],
    }