def parse_instance_name(resource_name: str):
    """Parses a GCE instance resource name."""

    if not resource_name.startswith("//"):
        resource_name = (
            "//compute.googleapis.com/"
            + resource_name
        )

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "zone": parts[6],
        "instance": parts[8],
    }

def parse_disk_name(resource_name: str):
    """Parses a GCE disk resource name."""

    if not resource_name.startswith("//"):
        resource_name = (
            "//compute.googleapis.com/"
            + resource_name
        )

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "zone": parts[6],
        "disk": parts[8],
    }

def parse_address_name(resource_name: str):

    if not resource_name.startswith("//"):
        resource_name = (
            "//compute.googleapis.com/"
            + resource_name
        )

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "region": parts[6],
        "address": parts[8],
    }


def parse_forwarding_rule_name(resource_name: str):

    if not resource_name.startswith("//"):
        resource_name = (
            "//compute.googleapis.com/"
            + resource_name
        )

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "region": parts[6],
        "forwarding_rule": parts[8],
    }

def parse_instance_template_name(resource_name: str):
    """Parses a Compute Instance Template."""

    if not resource_name.startswith("//"):
        resource_name = (
            "//compute.googleapis.com/"
            + resource_name
        )

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "instance_template": parts[6],
    }


def parse_instance_group_manager_name(resource_name: str):
    """Parses a Compute Instance Group Manager."""

    if not resource_name.startswith("//"):
        resource_name = (
            "//compute.googleapis.com/"
            + resource_name
        )

    parts = resource_name.split("/")

    return {
        "project": parts[4],
        "zone": parts[6],
        "instance_group_manager": parts[8],
    }