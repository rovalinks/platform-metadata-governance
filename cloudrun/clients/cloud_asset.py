from google.cloud import asset_v1


class CloudAssetClient:
    """Wrapper around the Google Cloud Asset Inventory client."""

    def __init__(self):
        self.client = asset_v1.AssetServiceClient()

    def list_assets(self, project_id: str):
        """
        List all assets within a Google Cloud project.
        """

        request = asset_v1.ListAssetsRequest(
            parent=f"projects/{project_id}",
            content_type=asset_v1.ContentType.RESOURCE,
        )

        return self.client.list_assets(request=request)