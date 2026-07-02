from googleapiclient.discovery import build

from clients.base import ResourceClient


class GkeClient(ResourceClient):
    """GKE Cluster adapter."""

    def __init__(self):

        self.client = build(
            "container",
            "v1",
            cache_discovery=False,
        )

    def supports(self, asset_type: str):

        return asset_type == "container.googleapis.com/Cluster"

    def labels(self, resource):

        info = self._parse(resource.name)

        cluster = (
            self.client.projects()
            .locations()
            .clusters()
            .get(
                name=info["name"]
            )
            .execute()
        )

        return dict(
            cluster.get(
                "resourceLabels",
                {}
            )
        )

    def apply_labels(self, resource, labels):

        info = self._parse(resource.name)

        cluster = (
            self.client.projects()
            .locations()
            .clusters()
            .get(
                name=info["name"]
            )
            .execute()
        )

        merged = dict(
            cluster.get(
                "resourceLabels",
                {}
            )
        )

        merged.update(labels)

        body = {
            "resourceLabels": merged,
            "labelFingerprint": cluster["labelFingerprint"]
        }

        (
            self.client.projects()
            .locations()
            .clusters()
            .resourceLabels(
                name=info["name"],
                body=body,
            )
            .execute()
        )

        return True

    @staticmethod
    def _parse(asset_name):

        #
        # //container.googleapis.com/projects/p/locations/r/clusters/c
        #

        name = asset_name.replace(
            "//container.googleapis.com/",
            ""
        )

        return {
            "name": name
        }