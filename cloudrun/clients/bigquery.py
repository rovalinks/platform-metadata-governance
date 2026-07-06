from google.cloud import bigquery

import config

from clients.base import ResourceClient
from models.resource import Resource
from utils.bigquery import (
    parse_dataset_name,
    parse_table_name,
)


class BigQueryClient(ResourceClient):
    """BigQuery Dataset and Table resource adapter."""

    def __init__(self):

        self.client = bigquery.Client()

    def supports(
        self,
        asset_type: str,
    ):

        return asset_type in (
            "bigquery.googleapis.com/Dataset",
            "bigquery.googleapis.com/Table",
        )

    def labels(
        self,
        resource,
    ):

        if (
            resource.asset_type
            == "bigquery.googleapis.com/Dataset"
        ):

            info = parse_dataset_name(
                resource.name
            )

            dataset = self.client.get_dataset(
                f"{info['project']}."
                f"{info['dataset']}"
            )

            return dict(
                dataset.labels or {}
            )

        info = parse_table_name(
            resource.name
        )

        table = self.client.get_table(
            f"{info['project']}."
            f"{info['dataset']}."
            f"{info['table']}"
        )

        return dict(
            table.labels or {}
        )

    def get(
        self,
        resource_name: str,
    ) -> Resource:
        """
        Retrieves a BigQuery dataset and returns
        the platform Resource model.

        Note:
        The public ResourceClient interface remains
        get(resource_name). Greenfield currently
        discovers datasets only.
        """

        info = parse_dataset_name(
            resource_name
        )

        dataset = self.client.get_dataset(
            f"{info['project']}."
            f"{info['dataset']}"
        )

        return Resource(

            asset_type="bigquery.googleapis.com/Dataset",

            name=resource_name,

            project=info["project"],

            location=dataset.location,

            labels=dict(
                dataset.labels or {}
            ),

            tags={},

        )

    def apply_labels(
        self,
        resource,
        labels: dict,
    ):

        if (
            resource.asset_type
            == "bigquery.googleapis.com/Dataset"
        ):

            info = parse_dataset_name(
                resource.name
            )

            dataset = self.client.get_dataset(
                f"{info['project']}."
                f"{info['dataset']}"
            )

            existing = dict(
                dataset.labels or {}
            )

            if config.PRESERVE_EXISTING_LABELS:

                merged = existing.copy()

                for key, value in labels.items():

                    if key not in merged:

                        merged[key] = value

            else:

                merged = existing.copy()

                merged.update(labels)

            if merged == existing:

                return True

            dataset.labels = merged

            self.client.update_dataset(
                dataset,
                ["labels"],
            )

            return True

        info = parse_table_name(
            resource.name
        )

        table = self.client.get_table(
            f"{info['project']}."
            f"{info['dataset']}."
            f"{info['table']}"
        )

        existing = dict(
            table.labels or {}
        )

        if config.PRESERVE_EXISTING_LABELS:

            merged = existing.copy()

            for key, value in labels.items():

                if key not in merged:

                    merged[key] = value

        else:

            merged = existing.copy()

            merged.update(labels)

        if merged == existing:

            return True

        table.labels = merged

        self.client.update_table(
            table,
            ["labels"],
        )

        return True