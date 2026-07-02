from google.cloud import storage

from clients.base import ResourceClient


class StorageClient(ResourceClient):
    """Cloud Storage resource adapter."""

    def __init__(self):

        self.client = storage.Client()

    def supports(self, asset_type: str):

        return asset_type == "storage.googleapis.com/Bucket"

    def labels(self, resource):

        bucket_name = resource.name.split("/")[-1]

        bucket = self.client.get_bucket(
            bucket_name
        )

        return dict(
            bucket.labels or {}
        )

    def apply_labels(self, resource, labels: dict):

        bucket_name = resource.name.split("/")[-1]

        bucket = self.client.get_bucket(
            bucket_name
        )

        merged = dict(
            bucket.labels or {}
        )

        merged.update(labels)

        bucket.labels = merged

        bucket.patch()

        return True