from google.cloud import compute_v1
import logging
from clients.base import ResourceClient
from models.resource import Resource
import config
logger = logging.getLogger(__name__)

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

    def supports(self, asset_type: str):
        return asset_type in [
            "compute.googleapis.com/Instance",
            "compute.googleapis.com/Disk",
            "compute.googleapis.com/Address",
            "compute.googleapis.com/ForwardingRule",
            "compute.googleapis.com/NetworkEndpointGroup",
            "compute.googleapis.com/Snapshot",
            "compute.googleapis.com/Image",
            "compute.googleapis.com/MachineImage",
            "compute.googleapis.com/InstanceGroup",
            "compute.googleapis.com/TargetPool",
            "compute.googleapis.com/ResourcePolicy",
            "compute.googleapis.com/NetworkAttachment",
            "compute.googleapis.com/ServiceAttachment",
            "compute.googleapis.com/VpnGateway",
            "compute.googleapis.com/PacketMirroring",
            "compute.googleapis.com/ExternalVpnGateway",
        ]

    def labels(self, resource):
        logger.info("=" * 80)
        logger.info("Entering ComputeClient.labels()")
        logger.info("Resource = %s", resource.name)
        
        if "/snapshots/" in resource.name:
            info = parse_snapshot_name(resource.name)
            snapshot = self.snapshots.get(project=info["project"], snapshot=info["snapshot"])
            return dict(snapshot.labels or {})
        elif "/images/" in resource.name:
            info = parse_image_name(resource.name)
            image = self.images.get(project=info["project"], image=info["image"])
            return dict(image.labels or {})
        elif "/machineImages/" in resource.name:
            info = parse_machine_image_name(resource.name)
            machine_image = self.machine_images.get(project=info["project"], machine_image=info["machine_image"])
            return dict(machine_image.labels or {})
        elif "/instanceGroups/" in resource.name:
            info = parse_instance_group_name(resource.name)
            group = self.instance_groups.get(project=info["project"], zone=info["zone"], instance_group=info["instance_group"])
            return dict(group.labels or {})
        elif "/targetPools/" in resource.name:
            info = parse_target_pool_name(resource.name)
            pool = self.target_pools.get(project=info["project"], region=info["region"], target_pool=info["target_pool"])
            return dict(pool.labels or {})
        elif "/resourcePolicies/" in resource.name:
            info = parse_resource_policy_name(resource.name)
            policy = self.resource_policies.get(project=info["project"], region=info["region"], resource_policy=info["resource_policy"])
            return dict(policy.labels or {})
        elif "/networkAttachments/" in resource.name:
            info = parse_network_attachment_name(resource.name)
            attachment = self.network_attachments.get(project=info["project"], region=info["region"], network_attachment=info["network_attachment"])
            return dict(attachment.labels or {})
        elif "/serviceAttachments/" in resource.name:
            info = parse_service_attachment_name(resource.name)
            attachment = self.service_attachments.get(project=info["project"], region=info["region"], service_attachment=info["service_attachment"])
            return dict(attachment.labels or {})
        elif "/vpnGateways/" in resource.name:
            info = parse_vpn_gateway_name(resource.name)
            gateway = self.vpn_gateways.get(project=info["project"], region=info["region"], vpn_gateway=info["vpn_gateway"])
            return dict(gateway.labels or {})
        elif "/packetMirrorings/" in resource.name:
            info = parse_packet_mirroring_name(resource.name)
            mirroring = self.packet_mirroring.get(project=info["project"], region=info["region"], packet_mirroring=info["packet_mirroring"])
            return dict(mirroring.labels or {})
        elif "/externalVpnGateways/" in resource.name:
            info = parse_external_vpn_gateway_name(resource.name)
            gateway = self.external_vpn_gateways.get(project=info["project"], external_vpn_gateway=info["external_vpn_gateway"])
            return dict(gateway.labels or {})
        elif "/instances/" in resource.name:
            info = parse_instance_name(resource.name)
            instance = self.instances.get(project=info["project"], zone=info["zone"], instance=info["instance"])
            return dict(instance.labels or {})
        elif "/disks/" in resource.name:
            info = parse_disk_name(resource.name)
            disk = self.disks.get(project=info["project"], zone=info["zone"], disk=info["disk"])
            return dict(disk.labels or {})
        elif "/addresses/" in resource.name:
            info = parse_address_name(resource.name)
            address = self.addresses.get(project=info["project"], region=info["region"], address=info["address"])
            return dict(address.labels or {})
        elif "/forwardingRules/" in resource.name:
            info = parse_forwarding_rule_name(resource.name)
            rule = self.forwarding_rules.get(project=info["project"], region=info["region"], forwarding_rule=info["forwarding_rule"])
            return dict(rule.labels or {})
            
        logger.warning("Unsupported Compute resource for labels(): %s", resource.name)
        return None

    def get(self, resource_name: str) -> Resource:
        """Retrieves a Compute Engine resource."""
        if "/networkEndpointGroups/" in resource_name:
            info = parse_network_endpoint_group_name(resource_name)
            neg = self.network_endpoint_groups.get(project=info["project"], zone=info["zone"], network_endpoint_group=info["network_endpoint_group"])
            return Resource(asset_type="compute.googleapis.com/NetworkEndpointGroup", name=resource_name, project=info["project"], location=info["zone"], labels=dict(neg.labels or {}), tags={})
        
        if "/snapshots/" in resource_name:
            info = parse_snapshot_name(resource_name)
            snapshot = self.snapshots.get(project=info["project"], snapshot=info["snapshot"])
            return Resource(asset_type="compute.googleapis.com/Snapshot", name=resource_name, project=info["project"], location="global", labels=dict(snapshot.labels or {}), tags={})
        
        if "/images/" in resource_name:
            info = parse_image_name(resource_name)
            image = self.images.get(project=info["project"], image=info["image"])
            return Resource(asset_type="compute.googleapis.com/Image", name=resource_name, project=info["project"], location="global", labels=dict(image.labels or {}), tags={})
        
        if "/machineImages/" in resource_name:
            info = parse_machine_image_name(resource_name)
            machine_image = self.machine_images.get(project=info["project"], machine_image=info["machine_image"])
            return Resource(asset_type="compute.googleapis.com/MachineImage", name=resource_name, project=info["project"], location="global", labels=dict(machine_image.labels or {}), tags={})
            
        if "/instanceGroups/" in resource_name:
            info = parse_instance_group_name(resource_name)
            group = self.instance_groups.get(project=info["project"], zone=info["zone"], instance_group=info["instance_group"])
            return Resource(asset_type="compute.googleapis.com/InstanceGroup", name=resource_name, project=info["project"], location=info["zone"], labels=dict(group.labels or {}), tags={})
        
        if "/targetPools/" in resource_name:
            info = parse_target_pool_name(resource_name)
            pool = self.target_pools.get(project=info["project"], region=info["region"], target_pool=info["target_pool"])
            return Resource(asset_type="compute.googleapis.com/TargetPool", name=resource_name, project=info["project"], location=info["region"], labels=dict(pool.labels or {}), tags={})
        
        if "/resourcePolicies/" in resource_name:
            info = parse_resource_policy_name(resource_name)
            policy = self.resource_policies.get(project=info["project"], region=info["region"], resource_policy=info["resource_policy"])
            return Resource(asset_type="compute.googleapis.com/ResourcePolicy", name=resource_name, project=info["project"], location=info["region"], labels=dict(policy.labels or {}), tags={})
        
        if "/instances/" in resource_name:
            info = parse_instance_name(resource_name)
            instance = self.instances.get(project=info["project"], zone=info["zone"], instance=info["instance"])
            return Resource(asset_type="compute.googleapis.com/Instance", name=resource_name, project=info["project"], location=info["zone"], labels=dict(instance.labels or {}), tags={})
        
        if "/disks/" in resource_name:
            info = parse_disk_name(resource_name)
            disk = self.disks.get(project=info["project"], zone=info["zone"], disk=info["disk"])
            return Resource(asset_type="compute.googleapis.com/Disk", name=resource_name, project=info["project"], location=info["zone"], labels=dict(disk.labels or {}), tags={})
        
        if "/addresses/" in resource_name:
            info = parse_address_name(resource_name)
            address = self.addresses.get(project=info["project"], region=info["region"], address=info["address"])
            return Resource(asset_type="compute.googleapis.com/Address", name=resource_name, project=info["project"], location=info["region"], labels=dict(address.labels or {}), tags={})
        
        if "/forwardingRules/" in resource_name:
            info = parse_forwarding_rule_name(resource_name)
            forwarding_rule = self.forwarding_rules.get(project=info["project"], region=info["region"], forwarding_rule=info["forwarding_rule"])
            return Resource(asset_type="compute.googleapis.com/ForwardingRule", name=resource_name, project=info["project"], location=info["region"], labels=dict(forwarding_rule.labels or {}), tags={})
            
        raise ValueError(f"Unsupported Compute resource: {resource_name}")
    
    def apply_labels(self, resource, labels: dict):
        if "/networkEndpointGroups/" in resource.name:
            info = parse_network_endpoint_group_name(resource.name)
            neg = self.network_endpoint_groups.get(project=info["project"], zone=info["zone"], network_endpoint_group=info["network_endpoint_group"])
            existing = dict(neg.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.ZoneSetLabelsRequest(labels=merged, label_fingerprint=neg.label_fingerprint)
            operation = self.network_endpoint_groups.set_labels(project=info["project"], zone=info["zone"], resource=info["network_endpoint_group"], zone_set_labels_request_resource=request)
        elif "/snapshots/" in resource.name:
            info = parse_snapshot_name(resource.name)
            snapshot = self.snapshots.get(project=info["project"], snapshot=info["snapshot"])
            existing = dict(snapshot.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.GlobalSetLabelsRequest(labels=merged, label_fingerprint=snapshot.label_fingerprint)
            operation = self.snapshots.set_labels(project=info["project"], resource=info["snapshot"], global_set_labels_request_resource=request)
        elif "/images/" in resource.name:
            info = parse_image_name(resource.name)
            image = self.images.get(project=info["project"], image=info["image"])
            existing = dict(image.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.GlobalSetLabelsRequest(labels=merged, label_fingerprint=image.label_fingerprint)
            operation = self.images.set_labels(project=info["project"], resource=info["image"], global_set_labels_request_resource=request)
        elif "/machineImages/" in resource.name:
            info = parse_machine_image_name(resource.name)
            machine_image = self.machine_images.get(project=info["project"], machine_image=info["machine_image"])
            existing = dict(machine_image.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.GlobalSetLabelsRequest(labels=merged, label_fingerprint=machine_image.label_fingerprint)
            operation = self.machine_images.set_labels(project=info["project"], resource=info["machine_image"], global_set_labels_request_resource=request)
        elif "/instanceGroups/" in resource.name:
            info = parse_instance_group_name(resource.name)
            group = self.instance_groups.get(project=info["project"], zone=info["zone"], instance_group=info["instance_group"])
            existing = dict(group.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.ZoneSetLabelsRequest(labels=merged, label_fingerprint=group.label_fingerprint)
            operation = self.instance_groups.set_labels(project=info["project"], zone=info["zone"], resource=info["instance_group"], zone_set_labels_request_resource=request)
        elif "/targetPools/" in resource.name:
            info = parse_target_pool_name(resource.name)
            pool = self.target_pools.get(project=info["project"], region=info["region"], target_pool=info["target_pool"])
            existing = dict(pool.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.RegionSetLabelsRequest(labels=merged, label_fingerprint=pool.label_fingerprint)
            operation = self.target_pools.set_labels(project=info["project"], region=info["region"], resource=info["target_pool"], region_set_labels_request_resource=request)
        elif "/resourcePolicies/" in resource.name:
            info = parse_resource_policy_name(resource.name)
            policy = self.resource_policies.get(project=info["project"], region=info["region"], resource_policy=info["resource_policy"])
            existing = dict(policy.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.RegionSetLabelsRequest(labels=merged, label_fingerprint=policy.label_fingerprint)
            operation = self.resource_policies.set_labels(project=info["project"], region=info["region"], resource=info["resource_policy"], region_set_labels_request_resource=request)
        elif "/instances/" in resource.name:
            info = parse_instance_name(resource.name)
            instance = self.instances.get(project=info["project"], zone=info["zone"], instance=info["instance"])
            existing = dict(instance.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.InstancesSetLabelsRequest(labels=merged, label_fingerprint=instance.label_fingerprint)
            operation = self.instances.set_labels(project=info["project"], zone=info["zone"], instance=info["instance"], instances_set_labels_request_resource=request)
        elif "/disks/" in resource.name:
            info = parse_disk_name(resource.name)
            disk = self.disks.get(project=info["project"], zone=info["zone"], disk=info["disk"])
            existing = dict(disk.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.ZoneSetLabelsRequest(labels=merged, label_fingerprint=disk.label_fingerprint)
            operation = self.disks.set_labels(project=info["project"], zone=info["zone"], resource=info["disk"], zone_set_labels_request_resource=request)
        elif "/addresses/" in resource.name:
            info = parse_address_name(resource.name)
            address = self.addresses.get(project=info["project"], region=info["region"], address=info["address"])
            existing = dict(address.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.RegionSetLabelsRequest(labels=merged, label_fingerprint=address.label_fingerprint)
            operation = self.addresses.set_labels(project=info["project"], region=info["region"], resource=info["address"], region_set_labels_request_resource=request)
        elif "/forwardingRules/" in resource.name:
            info = parse_forwarding_rule_name(resource.name)
            rule = self.forwarding_rules.get(project=info["project"], region=info["region"], forwarding_rule=info["forwarding_rule"])
            existing = dict(rule.labels or {})
            merged = self._merge_labels(existing, labels)
            if merged == existing: return True
            request = compute_v1.RegionSetLabelsRequest(labels=merged, label_fingerprint=rule.label_fingerprint)
            operation = self.forwarding_rules.set_labels(project=info["project"], region=info["region"], resource=info["forwarding_rule"], region_set_labels_request_resource=request)
        else:
            raise ValueError(f"Unsupported Compute resource: {resource.name}")
        
        # Operation handling
        if ("/instances/" in resource.name or "/disks/" in resource.name or "/networkEndpointGroups/" in resource.name or "/instanceGroups/" in resource.name):
            self.zone_operations.wait(project=info["project"], zone=info["zone"], operation=operation.name)
        elif ("/snapshots/" in resource.name or "/images/" in resource.name or "/machineImages/" in resource.name):
            self.global_operations.wait(project=info["project"], operation=operation.name)
        else:
            self.region_operations.wait(project=info["project"], region=info["region"], operation=operation.name)
        return True

    def _merge_labels(self, existing, labels):
        merged = existing.copy()
        if config.PRESERVE_EXISTING_LABELS:
            for k, v in labels.items():
                if k not in merged: merged[k] = v
        else:
            merged.update(labels)
        return merged