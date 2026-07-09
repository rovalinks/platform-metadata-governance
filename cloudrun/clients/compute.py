from google.cloud import compute_v1
from google.api_core.exceptions import PreconditionFailed
import logging
from clients.base import ResourceClient
from models.resource import Resource
import config
from utils.compute import (
    parse_instance_name, parse_disk_name, parse_address_name,
    parse_forwarding_rule_name, parse_snapshot_name,
    parse_image_name, parse_machine_image_name,
    parse_instance_group_name, parse_target_pool_name,
    parse_resource_policy_name, parse_network_attachment_name,
    parse_service_attachment_name, parse_vpn_gateway_name,
    parse_packet_mirroring_name, parse_external_vpn_gateway_name,
    parse_network_endpoint_group_name,
)

logger = logging.getLogger(__name__)

class ComputeClient(ResourceClient):
    """Compute Engine resource adapter with centralized label management."""

    def __init__(self):
        self.instances = compute_v1.InstancesClient()
        self.disks = compute_v1.DisksClient()
        self.addresses = compute_v1.AddressesClient()
        self.forwarding_rules = compute_v1.ForwardingRulesClient()
        self.zone_operations = compute_v1.ZoneOperationsClient()
        self.region_operations = compute_v1.RegionOperationsClient()
        self.global_operations = compute_v1.GlobalOperationsClient()
        self.network_endpoint_groups = compute_v1.NetworkEndpointGroupsClient()
        self.snapshots = compute_v1.SnapshotsClient()
        self.images = compute_v1.ImagesClient()
        self.machine_images = compute_v1.MachineImagesClient()
        self.instance_groups = compute_v1.InstanceGroupsClient()
        self.target_pools = compute_v1.TargetPoolsClient()
        self.resource_policies = compute_v1.ResourcePoliciesClient()
        self.vpn_gateways = compute_v1.VpnGatewaysClient()
        self.network_attachments = compute_v1.NetworkAttachmentsClient()
        self.service_attachments = compute_v1.ServiceAttachmentsClient()
        self.packet_mirroring = compute_v1.PacketMirroringsClient()
        self.external_vpn_gateways = compute_v1.ExternalVpnGatewaysClient()

    def _merge_labels(self, existing, labels):
        merged = existing.copy()
        if config.PRESERVE_EXISTING_LABELS:
            for k, v in labels.items():
                if k not in merged: merged[k] = v
        else:
            merged.update(labels)
        return merged

    def _apply_labels_generic(self, getter, setter, waiter, request_cls, request_kwarg, labels, **api_params):
        """Generic helper to handle Get-Merge-Check-Set cycle with retry."""
        def attempt():
            resource = getter()
            existing = dict(resource.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return None
            
            request = request_cls(labels=merged, label_fingerprint=resource.label_fingerprint)
            kwargs = {**api_params, f"{request_kwarg}_set_labels_request_resource": request}
            return setter(**kwargs)

        try:
            op = attempt()
        except PreconditionFailed:
            op = attempt()
            
        if op: waiter(op.name)
        return True

    def apply_labels(self, resource, labels: dict):
        if "/instances/" in resource.name:
            info = parse_instance_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.instances.get(project=info["project"], zone=info["zone"], instance=info["instance"]),
                self.instances.set_labels,
                lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op),
                compute_v1.InstancesSetLabelsRequest, "instances", labels,
                project=info["project"], zone=info["zone"], instance=info["instance"]
            )
        
        elif "/disks/" in resource.name:
            info = parse_disk_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.disks.get(project=info["project"], zone=info["zone"], disk=info["disk"]),
                self.disks.set_labels,
                lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op),
                compute_v1.ZoneSetLabelsRequest, "zone", labels,
                project=info["project"], zone=info["zone"], resource=info["disk"]
            )

        elif "/addresses/" in resource.name:
            info = parse_address_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.addresses.get(project=info["project"], region=info["region"], address=info["address"]),
                self.addresses.set_labels,
                lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op),
                compute_v1.RegionSetLabelsRequest, "region", labels,
                project=info["project"], region=info["region"], resource=info["address"]
            )

        elif "/forwardingRules/" in resource.name:
            info = parse_forwarding_rule_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.forwarding_rules.get(project=info["project"], region=info["region"], forwarding_rule=info["forwarding_rule"]),
                self.forwarding_rules.set_labels,
                lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op),
                compute_v1.RegionSetLabelsRequest, "region", labels,
                project=info["project"], region=info["region"], resource=info["forwarding_rule"]
            )

        elif "/networkEndpointGroups/" in resource.name:
            info = parse_network_endpoint_group_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.network_endpoint_groups.get(project=info["project"], zone=info["zone"], network_endpoint_group=info["network_endpoint_group"]),
                self.network_endpoint_groups.set_labels,
                lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op),
                compute_v1.ZoneSetLabelsRequest, "zone", labels,
                project=info["project"], zone=info["zone"], resource=info["network_endpoint_group"]
            )

        elif "/snapshots/" in resource.name:
            info = parse_snapshot_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.snapshots.get(project=info["project"], snapshot=info["snapshot"]),
                self.snapshots.set_labels,
                lambda op: self.global_operations.wait(project=info["project"], operation=op),
                compute_v1.GlobalSetLabelsRequest, "global", labels,
                project=info["project"], resource=info["snapshot"]
            )

        elif "/images/" in resource.name:
            info = parse_image_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.images.get(project=info["project"], image=info["image"]),
                self.images.set_labels,
                lambda op: self.global_operations.wait(project=info["project"], operation=op),
                compute_v1.GlobalSetLabelsRequest, "global", labels,
                project=info["project"], resource=info["image"]
            )

        elif "/machineImages/" in resource.name:
            info = parse_machine_image_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.machine_images.get(project=info["project"], machine_image=info["machine_image"]),
                self.machine_images.set_labels,
                lambda op: self.global_operations.wait(project=info["project"], operation=op),
                compute_v1.GlobalSetLabelsRequest, "global", labels,
                project=info["project"], resource=info["machine_image"]
            )

        elif "/instanceGroups/" in resource.name:
            info = parse_instance_group_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.instance_groups.get(project=info["project"], zone=info["zone"], instance_group=info["instance_group"]),
                self.instance_groups.set_labels,
                lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op),
                compute_v1.ZoneSetLabelsRequest, "zone", labels,
                project=info["project"], zone=info["zone"], resource=info["instance_group"]
            )

        elif "/targetPools/" in resource.name:
            info = parse_target_pool_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.target_pools.get(project=info["project"], region=info["region"], target_pool=info["target_pool"]),
                self.target_pools.set_labels,
                lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op),
                compute_v1.RegionSetLabelsRequest, "region", labels,
                project=info["project"], region=info["region"], resource=info["target_pool"]
            )

        elif "/resourcePolicies/" in resource.name:
            info = parse_resource_policy_name(resource.name)
            return self._apply_labels_generic(
                lambda: self.resource_policies.get(project=info["project"], region=info["region"], resource_policy=info["resource_policy"]),
                self.resource_policies.set_labels,
                lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op),
                compute_v1.RegionSetLabelsRequest, "region", labels,
                project=info["project"], region=info["region"], resource=info["resource_policy"]
            )

        else:
            raise ValueError(f"Unsupported Compute resource: {resource.name}")