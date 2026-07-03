from google.cloud import compute_v1
from google.api_core.exceptions import PreconditionFailed
import time

from clients.base import ResourceClient
from models.resource import Resource
from utils.compute import parse_instance_name, parse_disk_name

class ComputeClient(ResourceClient):
    """Compute Engine resource adapter."""

    def __init__(self):
        self.instances = compute_v1.InstancesClient()
        self.disks = compute_v1.DisksClient()
        self.zone_operations = compute_v1.ZoneOperationsClient()

    def supports(self, asset_type: str):
        # We keep this for the AdapterService lookup, 
        # but logic inside uses resource.name
        return asset_type in [
            "compute.googleapis.com/Instance",
            "compute.googleapis.com/Disk",
        ]

    def labels(self, resource):
        if "/instances/" in resource.name:
            info = parse_instance_name(resource.name)
            instance = self.instances.get(
                project=info["project"],
                zone=info["zone"],
                instance=info["instance"],
            )
            return dict(instance.labels or {})
        
        elif "/disks/" in resource.name:
            info = parse_disk_name(resource.name)
            disk = self.disks.get(
                project=info["project"],
                zone=info["zone"],
                disk=info["disk"],
            )
            return dict(disk.labels or {})

        raise ValueError(f"Unsupported Compute resource: {resource.name}")

    def get(
        self,
        resource_name: str,
    ) -> Resource:
        """
        Retrieves a Compute Engine resource and
        returns the platform Resource model.
        """

        if "/instances/" in resource_name:

            info = parse_instance_name(
                resource_name
            )

            instance = self.instances.get(
                project=info["project"],
                zone=info["zone"],
                instance=info["instance"],
            )

            return Resource(

                asset_type="compute.googleapis.com/Instance",

                name=resource_name,

                project=info["project"],

                location=info["zone"],

                labels=dict(
                    instance.labels or {}
                ),

                tags={},

            )

        if "/disks/" in resource_name:

            info = parse_disk_name(
                resource_name
            )

            disk = self.disks.get(
                project=info["project"],
                zone=info["zone"],
                disk=info["disk"],
            )

            return Resource(

                asset_type="compute.googleapis.com/Disk",

                name=resource_name,

                project=info["project"],

                location=info["zone"],

                labels=dict(
                    disk.labels or {}
                ),

                tags={},

            )

        raise ValueError(
            f"Unsupported Compute resource: "
            f"{resource_name}"
        )

    def apply_labels(self, resource, labels: dict):
        if "/instances/" in resource.name:
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
            
        elif "/disks/" in resource.name:
            info = parse_disk_name(resource.name)

            merged = labels.copy()

            for attempt in range(3):

                disk = self.disks.get(
                    project=info["project"],
                    zone=info["zone"],
                    disk=info["disk"],
                )

                merged = dict(disk.labels or {})
                merged.update(labels)

                request = compute_v1.ZoneSetLabelsRequest(
                    labels=merged,
                    label_fingerprint=disk.label_fingerprint,
                )

                try:

                    operation = self.disks.set_labels(
                        project=info["project"],
                        zone=info["zone"],
                        resource=info["disk"],
                        zone_set_labels_request_resource=request,
                    )

                    self.zone_operations.wait(
                        project=info["project"],
                        zone=info["zone"],
                        operation=operation.name,
                    )

                    return True

                except PreconditionFailed:

                    if attempt == 2:
                        raise

                    time.sleep(2)
        else:
            raise ValueError(f"Unsupported Compute resource: {resource.name}")

        # Wait for the operation to complete
        self.zone_operations.wait(
            project=info["project"],
            zone=info["zone"],
            operation=operation.name,
        )

        return True