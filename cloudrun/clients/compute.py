from google.cloud import compute_v1
from google.api_core.exceptions import PreconditionFailed
import time
from clients.base import ResourceClient
from models.resource import Resource
from utils.compute import ( parse_instance_name, parse_disk_name, parse_address_name, parse_forwarding_rule_name, parse_subnetwork_name, parse_health_check_name, parse_backend_service_name, parse_network_endpoint_group_name,
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
        self.global_operations = compute_v1.GlobalOperationsClient()
        self.subnetworks = compute_v1.SubnetworksClient()
        self.health_checks = compute_v1.HealthChecksClient()
        self.backend_services = compute_v1.BackendServicesClient()
        self.network_endpoint_groups = compute_v1.NetworkEndpointGroupsClient()

    def supports(self, asset_type: str):
        return asset_type in [
            "compute.googleapis.com/Instance",
            "compute.googleapis.com/Disk",
            "compute.googleapis.com/Address",
            "compute.googleapis.com/ForwardingRule",
            "compute.googleapis.com/Subnetwork",
            "compute.googleapis.com/HealthCheck",
            "compute.googleapis.com/BackendService",
            "compute.googleapis.com/NetworkEndpointGroup",
        ]
    def labels(self, resource):
        if "/subnetworks/" in resource.name:
            info = parse_subnetwork_name(
                resource.name
            )
            subnetwork = self.subnetworks.get(
                project=info["project"],
                region=info["region"],
                subnetwork=info["subnetwork"],
            )
            return dict(
                subnetwork.labels or {}
            )
        elif "/healthChecks/" in resource.name:
            info = parse_health_check_name(
                resource.name
            )
            health_check = self.health_checks.get(
                project=info["project"],
                health_check=info["health_check"],
            )
            return dict(
                health_check.labels or {}
            )
        elif "/networkEndpointGroups/" in resource.name:
            info = parse_network_endpoint_group_name(
                resource.name
            )
            neg = self.network_endpoint_groups.get(
                project=info["project"],
                zone=info["zone"],
                network_endpoint_group=info[
                    "network_endpoint_group"
                ],
            )
            return dict(
                neg.labels or {}
            )
        elif "/backendServices/" in resource.name:
            info = parse_backend_service_name(
                resource.name
            )
            backend = self.backend_services.get(
                project=info["project"],
                backend_service=info[
                    "backend_service"
                ],
            )
            return dict(
                backend.labels or {}
            )
        elif "/instances/" in resource.name:
            info = parse_instance_name(resource.name)
            instance = self.instances.get(
                project=info["project"],
                zone=info["zone"],
                instance=info["instance"],
            )
            return dict(
                instance.labels or {}
            )
        elif "/disks/" in resource.name:
            info = parse_disk_name(resource.name)
            disk = self.disks.get(
                project=info["project"],
                zone=info["zone"],
                disk=info["disk"],
            )
            return dict(
                disk.labels or {}
            )
        # Note: Add logic here if you need label support for
        # Address/ForwardingRule in the generic .labels() call
        raise ValueError(
            f"Unsupported Compute resource: {resource.name}"
        )
    def get(self, resource_name: str) -> Resource:
        """
        Retrieves a Compute Engine resource and
        returns the platform Resource model.
        """
        # Subnetwork
        if "/subnetworks/" in resource_name:
            info = parse_subnetwork_name(
                resource_name
            )
            subnetwork = self.subnetworks.get(
                project=info["project"],
                region=info["region"],
                subnetwork=info["subnetwork"],
            )
            return Resource(
                asset_type="compute.googleapis.com/Subnetwork",
                name=resource_name,
                project=info["project"],
                location=info["region"],
                labels=dict(
                    subnetwork.labels or {}
                ),
                tags={},
            )
        # Health Check
        if "/healthChecks/" in resource_name:
            info = parse_health_check_name(
                resource_name
            )
            health_check = self.health_checks.get(
                project=info["project"],
                health_check=info["health_check"],
            )
            return Resource(
                asset_type="compute.googleapis.com/HealthCheck",
                name=resource_name,
                project=info["project"],
                location="global",
                labels=dict(
                    health_check.labels or {}
                ),
                tags={},
            )
        # Backend Service
        if "/backendServices/" in resource_name:
            info = parse_backend_service_name(
                resource_name
            )
            backend = self.backend_services.get(
                project=info["project"],
                backend_service=info["backend_service"],
            )
            return Resource(
                asset_type="compute.googleapis.com/BackendService",
                name=resource_name,
                project=info["project"],
                location="global",
                labels=dict(
                    backend.labels or {}
                ),
                tags={},
            )
        # Network Endpoint Group
        if "/networkEndpointGroups/" in resource_name:
            info = parse_network_endpoint_group_name(
                resource_name
            )
            neg = self.network_endpoint_groups.get(
                project=info["project"],
                zone=info["zone"],
                network_endpoint_group=info[
                    "network_endpoint_group"
                ],
            )
            return Resource(
                asset_type="compute.googleapis.com/NetworkEndpointGroup",
                name=resource_name,
                project=info["project"],
                location=info["zone"],
                labels=dict(
                    neg.labels or {}
                ),
                tags={},
            )
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
        # Subnetwork
        if "/subnetworks/" in resource.name:
            info = parse_subnetwork_name(
                resource.name
            )
            subnetwork = self.subnetworks.get(
                project=info["project"],
                region=info["region"],
                subnetwork=info["subnetwork"],
            )
            existing = dict(
                subnetwork.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
            request = compute_v1.RegionSetLabelsRequest(
                labels=merged,
                label_fingerprint=subnetwork.label_fingerprint,
            )
            operation = self.subnetworks.set_labels(
                project=info["project"],
                region=info["region"],
                resource=info["subnetwork"],
                region_set_labels_request_resource=request,
            )
        # Health Check
        elif "/healthChecks/" in resource.name:
            info = parse_health_check_name(
                resource.name
            )
            health_check = self.health_checks.get(
                project=info["project"],
                health_check=info["health_check"],
            )
            existing = dict(
                health_check.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
            request = compute_v1.GlobalSetLabelsRequest(
                labels=merged,
                label_fingerprint=health_check.label_fingerprint,
            )
            operation = self.health_checks.set_labels(
                project=info["project"],
                resource=info["health_check"],
                global_set_labels_request_resource=request,
            )
        # Backend Service
        elif "/backendServices/" in resource.name:
            info = parse_backend_service_name(
                resource.name
            )
            backend = self.backend_services.get(
                project=info["project"],
                backend_service=info["backend_service"],
            )
            existing = dict(
                backend.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
            request = compute_v1.GlobalSetLabelsRequest(
                labels=merged,
                label_fingerprint=backend.label_fingerprint,
            )
            operation = self.backend_services.set_labels(
                project=info["project"],
                resource=info["backend_service"],
                global_set_labels_request_resource=request,
            )
        # Network Endpoint Group
        elif "/networkEndpointGroups/" in resource.name:
            info = parse_network_endpoint_group_name(
                resource.name
            )
            neg = self.network_endpoint_groups.get(
                project=info["project"],
                zone=info["zone"],
                network_endpoint_group=info[
                    "network_endpoint_group"
                ],
            )
            existing = dict(
                neg.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
            request = compute_v1.ZoneSetLabelsRequest(
                labels=merged,
                label_fingerprint=neg.label_fingerprint,
            )
            operation = self.network_endpoint_groups.set_labels(
                project=info["project"],
                zone=info["zone"],
                resource=info["network_endpoint_group"],
                zone_set_labels_request_resource=request,
            )
        if "/instances/" in resource.name:
            info = parse_instance_name(resource.name)
            instance = self.instances.get(
                project=info["project"],
                zone=info["zone"],
                instance=info["instance"],
            )
            existing = dict(
                instance.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
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
            disk = self.disks.get(
                project=info["project"],
                zone=info["zone"],
                disk=info["disk"],
            )
            existing = dict(
                disk.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
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
                project=info["project"],
                region=info["region"],
                address=info["address"],
            )
            existing = dict(
                address.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
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
                project=info["project"],
                region=info["region"],
                forwarding_rule=info["forwarding_rule"],
            )
            existing = dict(
                rule.labels or {}
            )
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key] = value
            else:
                merged = existing.copy()
                merged.update(labels)
            if merged == existing:
                return True
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
            raise ValueError(
                f"Unsupported Compute resource: {resource.name}"
            )
        # Zone resources
        if (
            "/instances/" in resource.name
            or "/disks/" in resource.name
            or "/networkEndpointGroups/" in resource.name
        ):
            self.zone_operations.wait(
                project=info["project"],
                zone=info["zone"],
                operation=operation.name,
            )
        # Global resources
        elif (
            "/healthChecks/" in resource.name
            or "/backendServices/" in resource.name
        ):
            self.global_operations.wait(
                project=info["project"],
                operation=operation.name,
            )
        # Regional resources
        else:
            self.region_operations.wait(
                project=info["project"],
                region=info["region"],
                operation=operation.name,
            )
        return True