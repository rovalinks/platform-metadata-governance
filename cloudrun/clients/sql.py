from googleapiclient.discovery import build

from clients.base import ResourceClient


class CloudSqlClient(ResourceClient):
    """Cloud SQL resource adapter."""

    def __init__(self):

        self.client = build(
            "sqladmin",
            "v1beta4",
            cache_discovery=False,
        )

    def supports(self, asset_type: str):

        return asset_type == "sqladmin.googleapis.com/Instance"

    def labels(self, resource):

        info = self._parse(resource.name)

        instance = (
            self.client.instances()
            .get(
                project=info["project"],
                instance=info["instance"],
            )
            .execute()
        )

        settings = instance.get("settings", {})

        return dict(
            settings.get(
                "userLabels",
                {},
            )
        )

    def apply_labels(self, resource, labels: dict):

        info = self._parse(resource.name)

        instance = (
            self.client.instances()
            .get(
                project=info["project"],
                instance=info["instance"],
            )
            .execute()
        )

        merged = dict(
            instance
            .get("settings", {})
            .get("userLabels", {})
        )

        merged.update(labels)

        body = {
            "settings": {
                "settingsVersion":
                    instance["settings"]["settingsVersion"],
                "userLabels":
                    merged,
            }
        }

        (
            self.client.instances()
            .patch(
                project=info["project"],
                instance=info["instance"],
                body=body,
            )
            .execute()
        )

        return True

    @staticmethod
    def _parse(name: str):

        #
        # //sqladmin.googleapis.com/projects/<project>/instances/<instance>
        #

        parts = name.split("/")

        return {
            "project": parts[4],
            "instance": parts[6],
        }
