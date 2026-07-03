from google.cloud import compute_v1
from google.api_core.exceptions import PreconditionFailed
import time

from clients.base import ResourceClient
from models.resource import Resource
from utils.compute import (
    parse_instance_name, 
    parse_disk_name, 
    parse_address_name, 
    parse_forwarding_rule_name
)

class ComputeClient(ResourceClient):
    """Compute Engine resource adapter."""

    def __init__(self):
        self.instances = compute_v1.InstancesClient()
        self.disks = compute_v1.DisksClient()
        self.addresses = compute_v1.AddressesClient()
        self.forwarding_rules = compute_v1.ForwardingRulesClient()
        self.zone_operations = compute_v1.ZoneOperationsClient()
        self.region_operations = compute_v1.RegionOperationsClient()

    def supports(self, asset_type: str):
        return asset_type in [
            "compute.googleapis.com/Instance",
            "compute.googleapis.com/Disk",
            "compute.googleapis.com/Address",
            "compute.googleapis.com/ForwardingRule",
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
        
        # Note: Add logic here if you need label support for Address/ForwardingRule in the generic .labels() call

        raise ValueError(f"Unsupported Compute resource: {resource.name}")

    def get(self, resource_name: str) -> Resource:
        """
        Retrieves a Compute Engine resource and
        returns the platform Resource model.
        """
        if "/instances/" in resource_name:
            info = parse_instance_name(resource_name)
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
                labels=dict(instance.labels or {}),
                tags={},
            )
            
        if "/disks/" in resource_name:
            info = parse_disk_name(resource_name)
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
                labels=dict(disk.labels or {}),
                tags={},
            )

        if "/addresses/" in resource_name:
            info = parse_address_name(resource_name)
            address = self.addresses.get(
                project=info["project"],
                region=info["region"],
                address=info["address"],
            )
            return Resource(
                asset_type="compute.googleapis.com/Address",
                name=resource_name,
                project=info["project"],
                location=info["region"],
                labels=dict(address.labels or {}),
                tags={},
            )

        if "/forwardingRules/" in resource_name:
            info = parse_forwarding_rule_name(resource_name)
            forwarding_rule = self.forwarding_rules.get(
                project=info["project"],
                region=info["region"],
                forwarding_rule=info["forwarding_rule"],
            )
            return Resource(
                asset_type="compute.googleapis.com/ForwardingRule",
                name=resource_name,
                project=info["project"],
                location=info["region"],
                labels=dict(forwarding_rule.labels or {}),
                tags={},
            )

        raise ValueError(f"Unsupported Compute resource: {resource_name}")

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
            disk = self.disks.get(project=info["project"], zone=info["zone"], disk=info["disk"])
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

        elif "/addresses/" in resource.name:
            info = parse_address_name(resource.name)
            address = self.addresses.get(
                project=info["project"], region=info["region"], address=info["address"],
            )
            merged = dict(address.labels or {})
            merged.update(labels)
            request = compute_v1.RegionSetLabelsRequest(
                labels=merged,
                label_fingerprint=address.label_fingerprint,
            )
            operation = self.addresses.set_labels(
                project=info["project"],
                region=info["region"],
                resource=info["address"],
                region_set_labels_request_resource=request,
            )

        elif "/forwardingRules/" in resource.name:
            info = parse_forwarding_rule_name(resource.name)
            rule = self.forwarding_rules.get(
                project=info["project"], region=info["region"], forwarding_rule=info["forwarding_rule"],
            )
            merged = dict(rule.labels or {})
            merged.update(labels)
            request = compute_v1.RegionSetLabelsRequest(
                labels=merged,
                label_fingerprint=rule.label_fingerprint,
            )
            operation = self.forwarding_rules.set_labels(
                project=info["project"],
                region=info["region"],
                resource=info["forwarding_rule"],
                region_set_labels_request_resource=request,
            )
        else:
            raise ValueError(f"Unsupported Compute resource: {resource.name}")

        # Wait for the operation to complete
        if "/instances/" in resource.name or "/disks/" in resource.name:
            self.zone_operations.wait(
                project=info["project"],
                zone=info["zone"],
                operation=operation.name,
            )
        else:
            self.region_operations.wait(
                project=info["project"],
                region=info["region"],
                operation=operation.name,
            )

        return True