from utils.logger import logger
from clients.cloud_asset import CloudAssetClient
from models.resource import Resource
from services.adapter import AdapterService
from repositories.snapshot_repository import SnapshotRepository


class DiscoveryService:
    """Discovers Google Cloud resources and enriches them with live metadata."""

    def __init__(self):
        self.client = CloudAssetClient()
        self.adapter = AdapterService()
        self.snapshot = SnapshotRepository()

    def discover(self, project_id: str):

        logger.info(
            "Starting resource discovery for project %s",
            project_id,
        )

        resources = []

        for asset in self.client.search_project_resources(project_id):

            resource = Resource(
                asset_type=asset.asset_type,
                name=asset.name,
                project=project_id,
                location=asset.location,
            )

            resource = self.adapter.enrich(resource)

            if resource is None:
                continue

            resources.append(resource)

        logger.info(
            "Discovered %d resources",
            len(resources),
        )

        run_id = self.snapshot.save_inventory(
            resources
        )

        logger.info(
            "Discovery snapshot saved. Run ID: %s",
            run_id,
        )

        return resources