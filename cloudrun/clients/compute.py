from clients.base import ResourceClient


class ComputeClient(ResourceClient):

    def supports(self, asset_type: str) -> bool:

        return asset_type == "compute.googleapis.com/Instance"

    def apply_labels(self, resource, labels: dict):

        raise NotImplementedError()