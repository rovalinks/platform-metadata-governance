from google.cloud import compute_v1

from clients.base import ResourceClient


class ComputeClient(ResourceClient):

    def __init__(self):

        self.instances = compute_v1.InstancesClient()

    def supports(self, asset_type: str):

        return asset_type == "compute.googleapis.com/Instance"

    def apply_labels(self, resource, labels: dict):

        raise NotImplementedError("Implementation added in next step.")