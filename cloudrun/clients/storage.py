from clients.base import ResourceClient


class StorageClient(ResourceClient):

    def supports(self, asset_type: str) -> bool:

        return asset_type == "storage.googleapis.com/Bucket"

    def apply_labels(self, resource, labels: dict):

        raise NotImplementedError()