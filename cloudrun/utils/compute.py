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

    def parse_subnetwork_name(
    resource_name: str,
):
    """
    projects/{project}/regions/{region}/subnetworks/{subnetwork}
    """
    parts = resource_name.split("/")

    return {
        "project": parts[1],
        "region": parts[3],
        "subnetwork": parts[5],
    }


def parse_health_check_name(
    resource_name: str,
):
    """
    projects/{project}/global/healthChecks/{health_check}
    """
    parts = resource_name.split("/")

    return {
        "project": parts[1],
        "health_check": parts[4],
    }


def parse_backend_service_name(
    resource_name: str,
):
    """
    projects/{project}/global/backendServices/{backend_service}
    """
    parts = resource_name.split("/")

    return {
        "project": parts[1],
        "backend_service": parts[4],
    }


def parse_network_endpoint_group_name(
    resource_name: str,
):
    """
    projects/{project}/zones/{zone}/networkEndpointGroups/{neg}
    """
    parts = resource_name.split("/")

    return {
        "project": parts[1],
        "zone": parts[3],
        "network_endpoint_group": parts[5],
    }