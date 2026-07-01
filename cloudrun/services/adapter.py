from clients.compute import ComputeClient
from clients.bigquery import BigQueryClient
# from clients.storage import StorageClient


class AdapterService:

    def __init__(self):
        self.clients = [
            ComputeClient(),
            BigQueryClient(),
            # StorageClient(),
        ]

    def client_for(self, asset_type: str):
        for client in self.clients:
            if client.supports(asset_type):
                return client
        return None

    def enrich(self, resource):
        """
        Populate a discovered resource with live metadata from the
        resource-specific Google Cloud API.
        """
        client = self.client_for(resource.asset_type)

        if client is None:
            return resource

        labels = client.labels(resource)

        if labels is not None:
            resource.labels = labels

        return resource