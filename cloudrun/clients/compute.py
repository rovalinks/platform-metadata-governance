from google.cloud import compute_v1
from clients.base import ResourceClient
from utils.compute import parse_instance_name


class ComputeClient(ResourceClient):

    def __init__(self):

        self.instances = compute_v1.InstancesClient()

        self.zone_operations = compute_v1.ZoneOperationsClient()

    def supports(self, asset_type: str):

        return asset_type == "compute.googleapis.com/Instance"

    def apply_labels(self, resource, labels: dict):

        info = parse_instance_name(resource.name)

        instance = self.instances.get(
            project=info["project"],
            zone=info["zone"],
            instance=info["instance"],
        )

        merged = dict(instance.labels)

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

        self.zone_operations.wait(
            project=info["project"],
            zone=info["zone"],
            operation=operation.name,
        )

        return True