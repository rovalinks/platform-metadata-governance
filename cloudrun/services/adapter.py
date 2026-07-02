from clients.compute import ComputeClient
from clients.bigquery import BigQueryClient
from clients.storage import StorageClient


class AdapterService:
    """Routes resources to the correct Google Cloud resource client."""

    def __init__(self):

        self.clients = [
            ComputeClient(),
            BigQueryClient(),
            StorageClient(),
        ]

    def client_for(self, asset_type: str):
        """
        Returns the client responsible for the supplied
        Cloud Asset Inventory asset type.
        """

        for client in self.clients:

            if client.supports(asset_type):
                return client

        return None

    def enrich(self, resource):
        """
        Enrich a discovered resource with live metadata
        from the Google Cloud service API.
        """

        client = self.client_for(resource.asset_type)

        if client is None:
            return resource

        labels = client.labels(resource)

        if labels is not None:
            resource.labels = labels

        return resource

    def apply_labels(self, resource, labels: dict):
        """
        Applies governance labels using the correct
        Google Cloud resource client.
        """

        client = self.client_for(resource.asset_type)

        if client is None:
            return False

        return client.apply_labels(resource, labels)