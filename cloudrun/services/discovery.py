from clients.cloud_asset import CloudAssetClient
from models.resource import Resource


class DiscoveryService:

    def __init__(self):
        self.client = CloudAssetClient()

    def discover(self, project_id: str):

        resources = []

        for asset in self.client.list_assets(project_id):

            resources.append(
                Resource(
                    asset_type=asset.asset_type,
                    name=asset.name,
                    project=project_id,
                    location=getattr(asset.resource, "location", None),
                    labels=dict(asset.resource.data.get("labels", {}))
                    if asset.resource and asset.resource.data
                    else {},
                )
            )

        return resources