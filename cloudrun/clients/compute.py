from google.cloud import compute_v1

from clients.base import ResourceClient
from utils.compute import parse_instance_name, parse_disk_name


class ComputeClient(ResourceClient):
    """Compute Engine resource adapter."""

    def __init__(self):
        self.instances = compute_v1.InstancesClient()
        self.disks = compute_v1.DisksClient()
        self.zone_operations = compute_v1.ZoneOperationsClient()

    def supports(self, asset_type: str):
        return asset_type in [
            "compute.googleapis.com/Instance",
            "compute.googleapis.com/Disk",
        ]

    def labels(self, resource):
        if resource.asset_type == "compute.googleapis.com/Instance":
            info = parse_instance_name(resource.name)
            instance = self.instances.get(
                project=info["project"],
                zone=info["zone"],
                instance=info["instance"],
            )
            return dict(instance.labels or {})
        
        elif resource.asset_type == "compute.googleapis.com/Disk":
            info = parse_disk_name(resource.name)
            disk = self.disks.get(
                project=info["project"],
                zone=info["zone"],
                disk=info["disk"],
            )
            return dict(disk.labels or {})

        return {}

    def apply_labels(self, resource, labels: dict):
        if resource.asset_type == "compute.googleapis.com/Instance":
            info = parse_instance_name(resource.name)
            instance = self.instances.get(
                project=info["project"], zone=info["zone"], instance=info["instance"]
            )
            
            merged = dict(instance.labels or {})
            merged.update(labels)
            
            request = compute_v1.InstancesSetLabelsRequest(
                labels=merged,
                label_fingerprint=instance.label_fingerprint,
            )
            operation = self.instances.set_labels(
                project=info["project"],
                zone=info["zone"],
                instance=info["instance"],
                instances_set_labels_request_resource=request,
            )
            
        elif resource.asset_type == "compute.googleapis.com/Disk":
            info = parse_disk_name(resource.name)
            disk = self.disks.get(
                project=info["project"], zone=info["zone"], disk=info["disk"]
            )
            
            merged = dict(disk.labels or {})
            merged.update(labels)
            
            request = compute_v1.ZoneSetLabelsRequest(
                labels=merged,
                label_fingerprint=disk.label_fingerprint,
            )
            operation = self.disks.set_labels(
                project=info["project"],
                zone=info["zone"],
                resource=info["disk"],
                zone_set_labels_request_resource=request,
            )
        else:
            return False

        # Wait for the operation to complete
        self.zone_operations.wait(
            project=info["project"],
            zone=info["zone"],
            operation=operation.name,
        )

        return True