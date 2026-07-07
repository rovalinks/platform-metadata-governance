import logging
from clients.compute import ComputeClient
from clients.bigquery import BigQueryClient
from clients.storage import StorageClient
from clients.sql import CloudSqlClient
from clients.artifact_registry import ArtifactRegistryClient
from clients.pubsub import PubSubClient
from clients.gke import GkeClient
from clients.bigquery_reservation import BigQueryReservationClient
from clients.secret_manager import SecretManagerClient
from clients.project import ProjectClient

logger = logging.getLogger(__name__)

class AdapterService:

    def __init__(self):
        self.clients = [
            # ComputeClient(),
            BigQueryClient(),
            BigQueryReservationClient(),
            StorageClient(),
            CloudSqlClient(),
            ArtifactRegistryClient(),
            PubSubClient(),
            GkeClient(),
            SecretManagerClient(),
            ProjectClient(),            
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
        client = self.client_for(resource.asset_type)

        if client is None:
            return resource

        try:
            labels = client.labels(resource)
        except Exception:
            logger.exception(
                "Failed to enrich %s",
                resource.asset_type,
            )
            return None

        if labels is None:
            return None

        resource.labels = labels

        return resource