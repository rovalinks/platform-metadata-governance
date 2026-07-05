from clients.compute import ComputeClient
from clients.bigquery import BigQueryClient
from clients.storage import StorageClient
from clients.sql import CloudSqlClient
from clients.artifact_registry import ArtifactRegistryClient
from clients.pubsub import PubSubClient
from clients.gke import GkeClient

class AdapterService:

    def __init__(self):

        self.clients = [
            ComputeClient(),
            BigQueryClient(),
            StorageClient(),
            CloudSqlClient(),
            ArtifactRegistryClient(),
            PubSubClient(),
            GkeClient(),            
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

        if labels is None:
            return None

        resource.labels = labels

        return resource