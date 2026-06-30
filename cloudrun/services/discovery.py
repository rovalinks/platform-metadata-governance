from utils.logger import logger
from clients.cloud_asset import CloudAssetClient
from models.resource import Resource

class DiscoveryService:

    def __init__(self):
        self.client = CloudAssetClient()

    def discover(self, project_id: str):
        logger.info(
            "Starting resource discovery for project %s",
            project_id,
        )

        resources = []

        for asset in self.client.search_project_resources(project_id):
            resources.append(
                Resource(
                    asset_type=asset.asset_type,
                    name=asset.name,
                    project=project_id,
                    location=asset.location,
                    labels=dict(asset.labels),
                )
            )

        logger.info(
            "Discovered %d resources",
            len(resources),
        )

        return resources