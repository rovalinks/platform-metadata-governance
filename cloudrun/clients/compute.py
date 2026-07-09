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
        """Generic helper to handle Get-Merge-Check-Set cycle with explicit retry."""
        
        def run_set():
            resource = getter()
            existing = dict(resource.labels or {})
            merged = self._merge_labels(existing, labels)
            
            if merged == existing:
                logger.info("Resource already compliant.")
                return True
                
            request = request_cls(labels=merged, label_fingerprint=resource.label_fingerprint)
            kwargs = {**api_params, f"{request_kwarg}_set_labels_request_resource": request}
            return setter(**kwargs)

        try:
            op = run_set()
        except PreconditionFailed:
            # Explicit Retry
            op = run_set()

        if op and op is not True:
            waiter(op.name)
        return True

    def apply_labels(self, resource, labels: dict):
        # Resource Dispatcher
        configs = {
            "/instances/": (self.instances.get, self.instances.set_labels, lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op), compute_v1.InstancesSetLabelsRequest, "instances", parse_instance_name),
            "/disks/": (self.disks.get, self.disks.set_labels, lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op), compute_v1.ZoneSetLabelsRequest, "zone", parse_disk_name),
            "/addresses/": (self.addresses.get, self.addresses.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_address_name),
            "/forwardingRules/": (self.forwarding_rules.get, self.forwarding_rules.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_forwarding_rule_name),
            "/networkEndpointGroups/": (self.network_endpoint_groups.get, self.network_endpoint_groups.set_labels, lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op), compute_v1.ZoneSetLabelsRequest, "zone", parse_network_endpoint_group_name),
            "/snapshots/": (self.snapshots.get, self.snapshots.set_labels, lambda op: self.global_operations.wait(project=info["project"], operation=op), compute_v1.GlobalSetLabelsRequest, "global", parse_snapshot_name),
            "/images/": (self.images.get, self.images.set_labels, lambda op: self.global_operations.wait(project=info["project"], operation=op), compute_v1.GlobalSetLabelsRequest, "global", parse_image_name),
            "/machineImages/": (self.machine_images.get, self.machine_images.set_labels, lambda op: self.global_operations.wait(project=info["project"], operation=op), compute_v1.GlobalSetLabelsRequest, "global", parse_machine_image_name),
            "/instanceGroups/": (self.instance_groups.get, self.instance_groups.set_labels, lambda op: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op), compute_v1.ZoneSetLabelsRequest, "zone", parse_instance_group_name),
            "/targetPools/": (self.target_pools.get, self.target_pools.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_target_pool_name),
            "/resourcePolicies/": (self.resource_policies.get, self.resource_policies.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_resource_policy_name),
            "/networkAttachments/": (self.network_attachments.get, self.network_attachments.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_network_attachment_name),
            "/serviceAttachments/": (self.service_attachments.get, self.service_attachments.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_service_attachment_name),
            "/vpnGateways/": (self.vpn_gateways.get, self.vpn_gateways.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_vpn_gateway_name),
            "/packetMirroring/": (self.packet_mirroring.get, self.packet_mirroring.set_labels, lambda op: self.region_operations.wait(project=info["project"], region=info["region"], operation=op), compute_v1.RegionSetLabelsRequest, "region", parse_packet_mirroring_name),
            "/externalVpnGateways/": (self.external_vpn_gateways.get, self.external_vpn_gateways.set_labels, lambda op: self.global_operations.wait(project=info["project"], operation=op), compute_v1.GlobalSetLabelsRequest, "global", parse_external_vpn_gateway_name),
        }

        for path, (getter, setter, waiter, req_cls, kwarg, parser) in configs.items():
            if path in resource.name:
                info = parser(resource.name)
                # Filter info to only required API arguments
                api_params = {k: v for k, v in info.items() if k in ["project", "zone", "region", "instance", "disk", "address", "forwarding_rule", "network_endpoint_group", "snapshot", "image", "machine_image", "instance_group", "target_pool", "resource_policy", "network_attachment", "service_attachment", "vpn_gateway", "packet_mirroring", "external_vpn_gateway"]}
                return self._apply_labels_generic(
                    getter=lambda: getter(**api_params),
                    setter=setter,
                    waiter=waiter,
                    request_cls=req_cls,
                    request_kwarg=kwarg,
                    labels=labels,
                    **api_params
                )
        
        raise ValueError(f"Unsupported Compute resource: {resource.name}")