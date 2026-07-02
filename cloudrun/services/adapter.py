from clients.compute import ComputeClient
from clients.bigquery import BigQueryClient
from clients.storage import StorageClient
from clients.sql import CloudSqlClient
from clients.artifact_registry import ArtifactRegistryClient

class AdapterService:

    def __init__(self):

        self.clients = [
            ComputeClient(),
            BigQueryClient(),
            StorageClient(),
            CloudSqlClient(),
            ArtifactRegistryClient(),
        ]

    def client_for(self, asset_type: str):

        for client in self.clients:

            if client.supports(asset_type):
                return client

        return None

    def enrich(self, resource):
        """
        Populate a discovered resource with live metadata.
        """

        client = self.client_for(
            resource.asset_type
        )

        if client is None:
            return resource

        labels = client.labels(resource)

        if labels is not None:
            resource.labels = labels

        return resource
