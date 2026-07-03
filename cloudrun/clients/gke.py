from google.cloud import container_v1

from clients.base import ResourceClient
from models.resource import Resource


class GkeClient(ResourceClient):
    """Google Kubernetes Engine resource adapter."""

    def __init__(self):

        self.client = (
            container_v1.ClusterManagerClient()
        )

    def supports(
        self,
        asset_type: str,
    ):

        return asset_type in [
            "container.googleapis.com/Cluster",
            "container.googleapis.com/NodePool",
        ]

    def labels(
        self,
        resource,
    ):

        if "/clusters/" in resource.name and "/nodePools/" not in resource.name:

            cluster = self.client.get_cluster(
                name=self._cluster_name(
                    resource.name
                )
            )

            return dict(
                cluster.resource_labels or {}
            )

        node_pool = self.client.get_node_pool(
            name=self._nodepool_name(
                resource.name
            )
        )

        return dict(
            node_pool.config.labels or {}
        )

    def get(
        self,
        resource_name: str,
    ) -> Resource:

        if "/clusters/" in resource_name and "/nodePools/" not in resource_name:

            cluster = self.client.get_cluster(
                name=self._cluster_name(
                    resource_name
                )
            )

            parts = resource_name.split("/")

            return Resource(

                asset_type="container.googleapis.com/Cluster",

                name=resource_name,

                project=parts[1],

                location=parts[3],

                labels=dict(
                    cluster.resource_labels or {}
                ),

                tags={},

            )

        node_pool = self.client.get_node_pool(
            name=self._nodepool_name(
                resource_name
            )
        )

        parts = resource_name.split("/")

        return Resource(

            asset_type="container.googleapis.com/NodePool",

            name=resource_name,

            project=parts[1],

            location=parts[3],

            labels=dict(
                node_pool.config.labels or {}
            ),

            tags={},

        )

    def apply_labels(
        self,
        resource,
        labels: dict,
    ):

        #
        # Cluster
        #

        if "/clusters/" in resource.name and "/nodePools/" not in resource.name:

            cluster = self.client.get_cluster(
                name=self._cluster_name(
                    resource.name
                )
            )

            merged = dict(
                cluster.resource_labels or {}
            )

            merged.update(labels)

            request = (
                container_v1.SetLabelsRequest(

                    name=cluster.name,

                    resource_labels=merged,

                    label_fingerprint=cluster.label_fingerprint,

                )
            )

            self.client.set_labels(
                request=request
            )

            return True

        #
        # Node Pool
        #

        node_pool = self.client.get_node_pool(
            name=self._nodepool_name(
                resource.name
            )
        )

        merged = dict(
            node_pool.config.labels or {}
        )

        merged.update(labels)

        request = (
            container_v1.UpdateNodePoolRequest(

                name=node_pool.name,

                node_labels=merged,

            )
        )

        self.client.update_node_pool(
            request=request
        )

        return True

    @staticmethod
    def _cluster_name(
        asset_name: str,
    ):

        return asset_name.replace(
            "//container.googleapis.com/",
            ""
        )

    @staticmethod
    def _nodepool_name(
        asset_name: str,
    ):

        return asset_name.replace(
            "//container.googleapis.com/",
            ""
        )