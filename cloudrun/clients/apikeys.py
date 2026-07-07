from google.cloud import api_keys_v2

import config

from clients.base import ResourceClient
from models.resource import Resource


class ApiKeysClient(ResourceClient):
    """
    API Keys adapter.
    """

    def __init__(self):

        self.client = api_keys_v2.ApiKeysClient()

    def supports(
        self,
        asset_type: str,
    ):

        return (
            asset_type
            == "apikeys.googleapis.com/Key"
        )

    def labels(
        self,
        resource,
    ):

        key = self.client.get_key(
            name=resource.name.lstrip("/")
        )

        return dict(
            key.labels or {}
        )

    def get(
        self,
        resource_name: str,
    ) -> Resource:

        key = self.client.get_key(
            name=resource_name.lstrip("/")
        )

        project = (
            resource_name.split("/")[3]
        )

        return Resource(

            asset_type="apikeys.googleapis.com/Key",

            name=resource_name,

            project=project,

            location="global",

            labels=dict(
                key.labels or {}
            ),

            tags={},

        )

    def apply_labels(
        self,
        resource,
        labels: dict,
    ):

        key = self.client.get_key(
            name=resource.name.lstrip("/")
        )

        existing = dict(
            key.labels or {}
        )

        if config.PRESERVE_EXISTING_LABELS:

            merged = existing.copy()

            for k, v in labels.items():

                if k not in merged:

                    merged[k] = v

        else:

            merged = existing.copy()
            merged.update(labels)

        if merged == existing:

            return True

        key.labels = merged

        operation = self.client.update_key(

            key=key,

            update_mask={
                "paths": [
                    "labels",
                ]
            },

        )

        operation.result()

        return True
