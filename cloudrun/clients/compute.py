from google.cloud import compute_v1
from google.api_core.exceptions import PreconditionFailed
import time
from clients.base import ResourceClient
from models.resource import Resource
from utils.compute import (
    parse_instance_name, parse_disk_name, parse_address_name,
    parse_forwarding_rule_name, parse_subnetwork_name,
    parse_health_check_name, parse_backend_service_name,
    parse_network_endpoint_group_name, parse_firewall_name,
    parse_network_name, parse_snapshot_name,
    parse_image_name, parse_machine_image_name,
    parse_ssl_certificate_name, parse_ssl_policy_name,
    parse_target_http_proxy_name, parse_target_https_proxy_name,
    parse_url_map_name, parse_router_name,
    parse_instance_group_name, parse_instance_group_manager_name,
    parse_instance_template_name, parse_target_pool_name,
    parse_resource_policy_name, parse_target_vpn_gateway_name,
    parse_network_attachment_name, parse_service_attachment_name,
    parse_vpn_gateway_name, parse_packet_mirroring_name,
    parse_external_vpn_gateway_name,
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
        self.firewalls = compute_v1.FirewallsClient()
        self.networks = compute_v1.NetworksClient()
        self.snapshots = compute_v1.SnapshotsClient()
        self.images = compute_v1.ImagesClient()
        self.machine_images = compute_v1.MachineImagesClient()
        self.ssl_certificates = compute_v1.SslCertificatesClient()
        self.ssl_policies = compute_v1.SslPoliciesClient()
        self.target_http_proxies = compute_v1.TargetHttpProxiesClient()
        self.target_https_proxies = compute_v1.TargetHttpsProxiesClient()
        self.url_maps = compute_v1.UrlMapsClient()
        self.routers = compute_v1.RoutersClient()
        self.instance_groups = compute_v1.InstanceGroupsClient()
        self.instance_group_managers = compute_v1.InstanceGroupManagersClient()
        self.instance_templates = compute_v1.InstanceTemplatesClient()
        self.target_pools = compute_v1.TargetPoolsClient()
        self.resource_policies = compute_v1.ResourcePoliciesClient()
        self.target_vpn_gateways = compute_v1.TargetVpnGatewaysClient()
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
            "compute.googleapis.com/Subnetwork",
            "compute.googleapis.com/HealthCheck",
            "compute.googleapis.com/BackendService",
            "compute.googleapis.com/NetworkEndpointGroup",
            "compute.googleapis.com/Firewall",
            "compute.googleapis.com/Network",
            "compute.googleapis.com/Snapshot",
            "compute.googleapis.com/Image",
            "compute.googleapis.com/MachineImage",
            "compute.googleapis.com/SslCertificate",
            "compute.googleapis.com/SslPolicy",
            "compute.googleapis.com/TargetHttpProxy",
            "compute.googleapis.com/TargetHttpsProxy",
            "compute.googleapis.com/UrlMap",
            "compute.googleapis.com/Router",
            "compute.googleapis.com/InstanceGroup",
            "compute.googleapis.com/InstanceTemplate",
            "compute.googleapis.com/TargetPool",
            "compute.googleapis.com/ResourcePolicy",
            "compute.googleapis.com/TargetVpnGateway",
            "compute.googleapis.com/NetworkAttachment",
            "compute.googleapis.com/ServiceAttachment",
            "compute.googleapis.com/VpnGateway",
            "compute.googleapis.com/PacketMirroring",
            "compute.googleapis.com/ExternalVpnGateway",
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
        elif "/firewalls/" in resource.name:
            info = parse_firewall_name(resource.name)
            firewall = self.firewalls.get(project=info["project"], firewall=info["firewall"])
            return dict(firewall.labels or {})
        elif "/networks/" in resource.name:
            info = parse_network_name(resource.name)
            network = self.networks.get(project=info["project"], network=info["network"])
            return dict(network.labels or {})
        elif "/snapshots/" in resource.name:
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
        elif "/sslCertificates/" in resource.name:
            info=parse_ssl_certificate_name(resource.name)
            certificate=self.ssl_certificates.get(project=info["project"], ssl_certificate=info["ssl_certificate"])
            return dict(certificate.labels or {})
        elif "/sslPolicies/" in resource.name:
            info=parse_ssl_policy_name(resource.name)
            policy=self.ssl_policies.get(project=info["project"], ssl_policy=info["ssl_policy"])
            return dict(policy.labels or {})
        elif "/targetHttpProxies/" in resource.name:
            info=parse_target_http_proxy_name(resource.name)
            proxy=self.target_http_proxies.get(project=info["project"], target_http_proxy=info["target_http_proxy"])
            return dict(proxy.labels or {})
        elif "/targetHttpsProxies/" in resource.name:
            info=parse_target_https_proxy_name(resource.name)
            proxy=self.target_https_proxies.get(project=info["project"], target_https_proxy=info["target_https_proxy"])
            return dict(proxy.labels or {})
        elif "/urlMaps/" in resource.name:
            info=parse_url_map_name(resource.name)
            url_map=self.url_maps.get(project=info["project"], url_map=info["url_map"])
            return dict(url_map.labels or {})
        elif "/routers/" in resource.name:
            info=parse_router_name(resource.name)
            router=self.routers.get(project=info["project"], region=info["region"], router=info["router"])
            return dict(router.labels or {})
        elif "/instanceGroups/" in resource.name:
            info=parse_instance_group_name(resource.name)
            group=self.instance_groups.get(project=info["project"],zone=info["zone"],instance_group=info["instance_group"])
            return dict(group.labels or {})
        elif "/targetPools/" in resource.name:
            info=parse_target_pool_name(resource.name)
            pool=self.target_pools.get(project=info["project"],region=info["region"],target_pool=info["target_pool"])
            return dict(pool.labels or {})
        elif "/resourcePolicies/" in resource.name:
            info=parse_resource_policy_name(resource.name)
            policy=self.resource_policies.get(project=info["project"],region=info["region"],resource_policy=info["resource_policy"])
            return dict(policy.labels or {})
        elif "/targetVpnGateways/" in resource.name:
            info=parse_target_vpn_gateway_name(resource.name)
            gateway=self.target_vpn_gateways.get(project=info["project"],region=info["region"],target_vpn_gateway=info["target_vpn_gateway"])
            return dict(gateway.labels or {})
        elif "/networkAttachments/" in resource.name:
            info=parse_network_attachment_name(resource.name)
            attachment=self.network_attachments.get(project=info["project"],region=info["region"],network_attachment=info["network_attachment"])
            return dict(attachment.labels or {})
        elif "/serviceAttachments/" in resource.name:
            info=parse_service_attachment_name(resource.name)
            attachment=self.service_attachments.get(project=info["project"],region=info["region"],service_attachment=info["service_attachment"])
            return dict(attachment.labels or {})
        elif "/vpnGateways/" in resource.name:
            info=parse_vpn_gateway_name(resource.name)
            gateway=self.vpn_gateways.get(project=info["project"],region=info["region"],vpn_gateway=info["vpn_gateway"])
            return dict(gateway.labels or {})
        elif "/packetMirrorings/" in resource.name:
            info=parse_packet_mirroring_name(resource.name)
            mirroring=self.packet_mirroring.get(project=info["project"],region=info["region"],packet_mirroring=info["packet_mirroring"])
            return dict(mirroring.labels or {})
        elif "/externalVpnGateways/" in resource.name:
            info=parse_external_vpn_gateway_name(resource.name)
            gateway=self.external_vpn_gateways.get(project=info["project"],external_vpn_gateway=info["external_vpn_gateway"])
            return dict(gateway.labels or {})
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
        # Firewall
        if "/firewalls/" in resource_name:
            info = parse_firewall_name(resource_name)
            firewall = self.firewalls.get(project=info["project"], firewall=info["firewall"])
            return Resource(asset_type="compute.googleapis.com/Firewall", name=resource_name, project=info["project"], location="global", labels=dict(firewall.labels or {}), tags={})
        # Network
        if "/networks/" in resource_name:
            info = parse_network_name(resource_name)
            network = self.networks.get(project=info["project"], network=info["network"])
            return Resource(asset_type="compute.googleapis.com/Network", name=resource_name, project=info["project"], location="global", labels=dict(network.labels or {}), tags={})
        # Snapshot
        if "/snapshots/" in resource_name:
            info = parse_snapshot_name(resource_name)
            snapshot = self.snapshots.get(project=info["project"], snapshot=info["snapshot"])
            return Resource(asset_type="compute.googleapis.com/Snapshot", name=resource_name, project=info["project"], location="global", labels=dict(snapshot.labels or {}), tags={})
        # Image
        if "/images/" in resource_name:
            info = parse_image_name(resource_name)
            image = self.images.get(project=info["project"], image=info["image"])
            return Resource(asset_type="compute.googleapis.com/Image", name=resource_name, project=info["project"], location="global", labels=dict(image.labels or {}), tags={})
        # Machine Image
        if "/machineImages/" in resource_name:
            info = parse_machine_image_name(resource_name)
            machine_image = self.machine_images.get(project=info["project"], machine_image=info["machine_image"])
            return Resource(asset_type="compute.googleapis.com/MachineImage", name=resource_name, project=info["project"], location="global", labels=dict(machine_image.labels or {}), tags={})
        # SSL Certificate
        if "/sslCertificates/" in resource_name:
            info=parse_ssl_certificate_name(resource_name)
            certificate=self.ssl_certificates.get(project=info["project"], ssl_certificate=info["ssl_certificate"])
            return Resource(asset_type="compute.googleapis.com/SslCertificate", name=resource_name, project=info["project"], location="global", labels=dict(certificate.labels or {}), tags={})
        # SSL Policy
        if "/sslPolicies/" in resource_name:
            info=parse_ssl_policy_name(resource_name)
            policy=self.ssl_policies.get(project=info["project"], ssl_policy=info["ssl_policy"])
            return Resource(asset_type="compute.googleapis.com/SslPolicy", name=resource_name, project=info["project"], location="global", labels=dict(policy.labels or {}), tags={})
        # Target HTTP Proxy
        if "/targetHttpProxies/" in resource_name:
            info=parse_target_http_proxy_name(resource_name)
            proxy=self.target_http_proxies.get(project=info["project"], target_http_proxy=info["target_http_proxy"])
            return Resource(asset_type="compute.googleapis.com/TargetHttpProxy", name=resource_name, project=info["project"], location="global", labels=dict(proxy.labels or {}), tags={})
        # Target HTTPS Proxy
        if "/targetHttpsProxies/" in resource_name:
            info=parse_target_https_proxy_name(resource_name)
            proxy=self.target_https_proxies.get(project=info["project"], target_https_proxy=info["target_https_proxy"])
            return Resource(asset_type="compute.googleapis.com/TargetHttpsProxy", name=resource_name, project=info["project"], location="global", labels=dict(proxy.labels or {}), tags={})
        # URL Map
        if "/urlMaps/" in resource_name:
            info=parse_url_map_name(resource_name)
            url_map=self.url_maps.get(project=info["project"], url_map=info["url_map"])
            return Resource(asset_type="compute.googleapis.com/UrlMap", name=resource_name, project=info["project"], location="global", labels=dict(url_map.labels or {}), tags={})
        # Router
        if "/routers/" in resource_name:
            info=parse_router_name(resource_name)
            router=self.routers.get(project=info["project"], region=info["region"], router=info["router"])
            return Resource(asset_type="compute.googleapis.com/Router", name=resource_name, project=info["project"], location=info["region"], labels=dict(router.labels or {}), tags={})

        if "/instanceGroups/" in resource_name:
            info=parse_instance_group_name(resource_name)
            group=self.instance_groups.get(project=info["project"],zone=info["zone"],instance_group=info["instance_group"])
            return Resource(asset_type="compute.googleapis.com/InstanceGroup",name=resource_name,project=info["project"],location=info["zone"],labels=dict(group.labels or {}),tags={})
        if "/targetPools/" in resource_name:
            info=parse_target_pool_name(resource_name)
            pool=self.target_pools.get(project=info["project"],region=info["region"],target_pool=info["target_pool"])
            return Resource(asset_type="compute.googleapis.com/TargetPool",name=resource_name,project=info["project"],location=info["region"],labels=dict(pool.labels or {}),tags={})
        if "/resourcePolicies/" in resource_name:
            info=parse_resource_policy_name(resource_name)
            policy=self.resource_policies.get(project=info["project"],region=info["region"],resource_policy=info["resource_policy"])
            return Resource(asset_type="compute.googleapis.com/ResourcePolicy",name=resource_name,project=info["project"],location=info["region"],labels=dict(policy.labels or {}),tags={})
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
        # Firewall
        elif "/firewalls/" in resource.name:
            info = parse_firewall_name(resource.name)
            firewall = self.firewalls.get(project=info["project"], firewall=info["firewall"])
            existing = dict(firewall.labels or {})
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
            request = compute_v1.GlobalSetLabelsRequest(labels=merged, label_fingerprint=firewall.label_fingerprint)
            operation = self.firewalls.set_labels(project=info["project"], resource=info["firewall"], global_set_labels_request_resource=request)
        # Network
        elif "/networks/" in resource.name:
            info = parse_network_name(resource.name)
            network = self.networks.get(project=info["project"], network=info["network"])
            existing = dict(network.labels or {})
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
            request = compute_v1.GlobalSetLabelsRequest(labels=merged, label_fingerprint=network.label_fingerprint)
            operation = self.networks.set_labels(project=info["project"], resource=info["network"], global_set_labels_request_resource=request)
        # Snapshot
        elif "/snapshots/" in resource.name:
            info = parse_snapshot_name(resource.name)
            snapshot = self.snapshots.get(project=info["project"], snapshot=info["snapshot"])
            existing = dict(snapshot.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged = existing.copy()
                for key, value in labels.items():
                    if key not in merged:
                        merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=snapshot.label_fingerprint)
            operation=self.snapshots.set_labels(project=info["project"],resource=info["snapshot"],global_set_labels_request_resource=request)
        # Image
        elif "/images/" in resource.name:
            info=parse_image_name(resource.name)
            image=self.images.get(project=info["project"],image=info["image"])
            existing=dict(image.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=image.label_fingerprint)
            operation=self.images.set_labels(project=info["project"],resource=info["image"],global_set_labels_request_resource=request)
        # Machine Image
        elif "/machineImages/" in resource.name:
            info=parse_machine_image_name(resource.name)
            machine_image=self.machine_images.get(project=info["project"],machine_image=info["machine_image"])
            existing=dict(machine_image.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=machine_image.label_fingerprint)
            operation=self.machine_images.set_labels(project=info["project"],resource=info["machine_image"],global_set_labels_request_resource=request)

        # SSL Certificate
        elif "/sslCertificates/" in resource.name:
            info=parse_ssl_certificate_name(resource.name)
            certificate=self.ssl_certificates.get(project=info["project"], ssl_certificate=info["ssl_certificate"])
            existing=dict(certificate.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=certificate.label_fingerprint)
            operation=self.ssl_certificates.set_labels(project=info["project"],resource=info["ssl_certificate"],global_set_labels_request_resource=request)
        # SSL Policy
        elif "/sslPolicies/" in resource.name:
            info=parse_ssl_policy_name(resource.name)
            policy=self.ssl_policies.get(project=info["project"], ssl_policy=info["ssl_policy"])
            existing=dict(policy.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=policy.label_fingerprint)
            operation=self.ssl_policies.set_labels(project=info["project"],resource=info["ssl_policy"],global_set_labels_request_resource=request)
        # Target HTTP Proxy
        elif "/targetHttpProxies/" in resource.name:
            info=parse_target_http_proxy_name(resource.name)
            proxy=self.target_http_proxies.get(project=info["project"], target_http_proxy=info["target_http_proxy"])
            existing=dict(proxy.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=proxy.label_fingerprint)
            operation=self.target_http_proxies.set_labels(project=info["project"],resource=info["target_http_proxy"],global_set_labels_request_resource=request)
        # Target HTTPS Proxy
        elif "/targetHttpsProxies/" in resource.name:
            info=parse_target_https_proxy_name(resource.name)
            proxy=self.target_https_proxies.get(project=info["project"], target_https_proxy=info["target_https_proxy"])
            existing=dict(proxy.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=proxy.label_fingerprint)
            operation=self.target_https_proxies.set_labels(project=info["project"],resource=info["target_https_proxy"],global_set_labels_request_resource=request)
        # URL Map
        elif "/urlMaps/" in resource.name:
            info=parse_url_map_name(resource.name)
            url_map=self.url_maps.get(project=info["project"], url_map=info["url_map"])
            existing=dict(url_map.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.GlobalSetLabelsRequest(labels=merged,label_fingerprint=url_map.label_fingerprint)
            operation=self.url_maps.set_labels(project=info["project"],resource=info["url_map"],global_set_labels_request_resource=request)
        # Router
        elif "/routers/" in resource.name:
            info=parse_router_name(resource.name)
            router=self.routers.get(project=info["project"], region=info["region"], router=info["router"])
            existing=dict(router.labels or {})
            if config.PRESERVE_EXISTING_LABELS:
                merged=existing.copy()
                for key,value in labels.items():
                    if key not in merged: merged[key]=value
            else:
                merged=existing.copy(); merged.update(labels)
            if merged==existing: return True
            request=compute_v1.RegionSetLabelsRequest(labels=merged,label_fingerprint=router.label_fingerprint)
            operation=self.routers.set_labels(project=info["project"],region=info["region"],resource=info["router"],region_set_labels_request_resource=request)


        elif "/instanceGroups/" in resource.name:
            info=parse_instance_group_name(resource.name)
            group=self.instance_groups.get(project=info["project"],zone=info["zone"],instance_group=info["instance_group"])
            existing=dict(group.labels or {})
            merged=existing.copy()
            if config.PRESERVE_EXISTING_LABELS:
                for k,v in labels.items():
                    if k not in merged: merged[k]=v
            else: merged.update(labels)
            if merged==existing:return True
            request=compute_v1.ZoneSetLabelsRequest(labels=merged,label_fingerprint=group.label_fingerprint)
            operation=self.instance_groups.set_labels(project=info["project"],zone=info["zone"],resource=info["instance_group"],zone_set_labels_request_resource=request)
        elif "/targetPools/" in resource.name:
            info=parse_target_pool_name(resource.name)
            pool=self.target_pools.get(project=info["project"],region=info["region"],target_pool=info["target_pool"])
            existing=dict(pool.labels or {})
            merged=existing.copy()
            if config.PRESERVE_EXISTING_LABELS:
                for k,v in labels.items():
                    if k not in merged: merged[k]=v
            else: merged.update(labels)
            if merged==existing:return True
            request=compute_v1.RegionSetLabelsRequest(labels=merged,label_fingerprint=pool.label_fingerprint)
            operation=self.target_pools.set_labels(project=info["project"],region=info["region"],resource=info["target_pool"],region_set_labels_request_resource=request)
        elif "/resourcePolicies/" in resource.name:
            info=parse_resource_policy_name(resource.name)
            policy=self.resource_policies.get(project=info["project"],region=info["region"],resource_policy=info["resource_policy"])
            existing=dict(policy.labels or {})
            merged=existing.copy()
            if config.PRESERVE_EXISTING_LABELS:
                for k,v in labels.items():
                    if k not in merged: merged[k]=v
            else: merged.update(labels)
            if merged==existing:return True
            request=compute_v1.RegionSetLabelsRequest(labels=merged,label_fingerprint=policy.label_fingerprint)
            operation=self.resource_policies.set_labels(project=info["project"],region=info["region"],resource=info["resource_policy"],region_set_labels_request_resource=request)
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
            or "/instanceGroups/" in resource.name
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
            or "/firewalls/" in resource.name
            or "/networks/" in resource.name
            or "/snapshots/" in resource.name
            or "/images/" in resource.name
            or "/machineImages/" in resource.name
            or "/sslCertificates/" in resource.name
            or "/sslPolicies/" in resource.name
            or "/targetHttpProxies/" in resource.name
            or "/targetHttpsProxies/" in resource.name
            or "/urlMaps/" in resource.name
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