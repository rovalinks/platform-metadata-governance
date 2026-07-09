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

    def _apply_labels_generic(self, getter, setter, request_cls, request_key, labels):
        def run_set():
            resource = getter()
            existing = dict(resource.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing:
                logger.info("Resource already compliant.")
                return True
            request = request_cls(labels=merged, label_fingerprint=resource.label_fingerprint)
            return setter(**{request_key: request})

        try:
            return run_set()
        except PreconditionFailed:
            return run_set()

    def apply_labels(self, resource, labels: dict):
        # 1. Instances
        if "/instances/" in resource.name:
            info = parse_instance_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.instances.get(project=info["project"], zone=info["zone"], instance=info["instance"]),
                lambda req: self.instances.set_labels(project=info["project"], zone=info["zone"], instance=info["instance"], instances_set_labels_request_resource=req),
                compute_v1.InstancesSetLabelsRequest, "instances_set_labels_request_resource", labels
            )
            if op and op is not True: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op.name)
        
        # 2. Disks
        elif "/disks/" in resource.name:
            info = parse_disk_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.disks.get(project=info["project"], zone=info["zone"], disk=info["disk"]),
                lambda req: self.disks.set_labels(project=info["project"], zone=info["zone"], resource=info["disk"], zone_set_labels_request_resource=req),
                compute_v1.ZoneSetLabelsRequest, "zone_set_labels_request_resource", labels
            )
            if op and op is not True: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op.name)

        # 3. Addresses
        elif "/addresses/" in resource.name:
            info = parse_address_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.addresses.get(project=info["project"], region=info["region"], address=info["address"]),
                lambda req: self.addresses.set_labels(project=info["project"], region=info["region"], resource=info["address"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 4. Forwarding Rules
        elif "/forwardingRules/" in resource.name:
            info = parse_forwarding_rule_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.forwarding_rules.get(project=info["project"], region=info["region"], forwarding_rule=info["forwarding_rule"]),
                lambda req: self.forwarding_rules.set_labels(project=info["project"], region=info["region"], resource=info["forwarding_rule"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 5. Network Endpoint Groups
        elif "/networkEndpointGroups/" in resource.name:
            info = parse_network_endpoint_group_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.network_endpoint_groups.get(project=info["project"], zone=info["zone"], network_endpoint_group=info["network_endpoint_group"]),
                lambda req: self.network_endpoint_groups.set_labels(project=info["project"], zone=info["zone"], resource=info["network_endpoint_group"], zone_set_labels_request_resource=req),
                compute_v1.ZoneSetLabelsRequest, "zone_set_labels_request_resource", labels
            )
            if op and op is not True: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op.name)

        # 6. Snapshots
        elif "/snapshots/" in resource.name:
            info = parse_snapshot_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.snapshots.get(project=info["project"], snapshot=info["snapshot"]),
                lambda req: self.snapshots.set_labels(project=info["project"], resource=info["snapshot"], global_set_labels_request_resource=req),
                compute_v1.GlobalSetLabelsRequest, "global_set_labels_request_resource", labels
            )
            if op and op is not True: self.global_operations.wait(project=info["project"], operation=op.name)

        # 7. Images
        elif "/images/" in resource.name:
            info = parse_image_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.images.get(project=info["project"], image=info["image"]),
                lambda req: self.images.set_labels(project=info["project"], resource=info["image"], global_set_labels_request_resource=req),
                compute_v1.GlobalSetLabelsRequest, "global_set_labels_request_resource", labels
            )
            if op and op is not True: self.global_operations.wait(project=info["project"], operation=op.name)

        # 8. Machine Images
        elif "/machineImages/" in resource.name:
            info = parse_machine_image_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.machine_images.get(project=info["project"], machine_image=info["machine_image"]),
                lambda req: self.machine_images.set_labels(project=info["project"], resource=info["machine_image"], global_set_labels_request_resource=req),
                compute_v1.GlobalSetLabelsRequest, "global_set_labels_request_resource", labels
            )
            if op and op is not True: self.global_operations.wait(project=info["project"], operation=op.name)

        # 9. Instance Groups
        elif "/instanceGroups/" in resource.name:
            info = parse_instance_group_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.instance_groups.get(project=info["project"], zone=info["zone"], instance_group=info["instance_group"]),
                lambda req: self.instance_groups.set_labels(project=info["project"], zone=info["zone"], resource=info["instance_group"], zone_set_labels_request_resource=req),
                compute_v1.ZoneSetLabelsRequest, "zone_set_labels_request_resource", labels
            )
            if op and op is not True: self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=op.name)

        # 10. Target Pools
        elif "/targetPools/" in resource.name:
            info = parse_target_pool_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.target_pools.get(project=info["project"], region=info["region"], target_pool=info["target_pool"]),
                lambda req: self.target_pools.set_labels(project=info["project"], region=info["region"], resource=info["target_pool"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 11. Resource Policies
        elif "/resourcePolicies/" in resource.name:
            info = parse_resource_policy_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.resource_policies.get(project=info["project"], region=info["region"], resource_policy=info["resource_policy"]),
                lambda req: self.resource_policies.set_labels(project=info["project"], region=info["region"], resource=info["resource_policy"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 12. Network Attachments
        elif "/networkAttachments/" in resource.name:
            info = parse_network_attachment_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.network_attachments.get(project=info["project"], region=info["region"], network_attachment=info["network_attachment"]),
                lambda req: self.network_attachments.set_labels(project=info["project"], region=info["region"], resource=info["network_attachment"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 13. Service Attachments
        elif "/serviceAttachments/" in resource.name:
            info = parse_service_attachment_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.service_attachments.get(project=info["project"], region=info["region"], service_attachment=info["service_attachment"]),
                lambda req: self.service_attachments.set_labels(project=info["project"], region=info["region"], resource=info["service_attachment"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 14. VPN Gateways
        elif "/vpnGateways/" in resource.name:
            info = parse_vpn_gateway_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.vpn_gateways.get(project=info["project"], region=info["region"], vpn_gateway=info["vpn_gateway"]),
                lambda req: self.vpn_gateways.set_labels(project=info["project"], region=info["region"], resource=info["vpn_gateway"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 15. Packet Mirroring
        elif "/packetMirrorings/" in resource.name:
            info = parse_packet_mirroring_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.packet_mirroring.get(project=info["project"], region=info["region"], packet_mirroring=info["packet_mirroring"]),
                lambda req: self.packet_mirroring.set_labels(project=info["project"], region=info["region"], resource=info["packet_mirroring"], region_set_labels_request_resource=req),
                compute_v1.RegionSetLabelsRequest, "region_set_labels_request_resource", labels
            )
            if op and op is not True: self.region_operations.wait(project=info["project"], region=info["region"], operation=op.name)

        # 16. External VPN Gateways
        elif "/externalVpnGateways/" in resource.name:
            info = parse_external_vpn_gateway_name(resource.name)
            op = self._apply_labels_generic(
                lambda: self.external_vpn_gateways.get(project=info["project"], external_vpn_gateway=info["external_vpn_gateway"]),
                lambda req: self.external_vpn_gateways.set_labels(project=info["project"], resource=info["external_vpn_gateway"], global_set_labels_request_resource=req),
                compute_v1.GlobalSetLabelsRequest, "global_set_labels_request_resource", labels
            )
            if op and op is not True: self.global_operations.wait(project=info["project"], operation=op.name)

        else:
            raise ValueError(f"Unsupported Compute resource: {resource.name}")
        
        return True