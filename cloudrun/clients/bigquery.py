from google.cloud import bigquery

import config

from clients.base import ResourceClient
from models.resource import Resource
from utils.bigquery import parse_dataset_name


class BigQueryClient(ResourceClient):
    """BigQuery Dataset resource adapter."""

    def __init__(self):

        self.client = bigquery.Client()

    def supports(
        self,
        asset_type: str,
    ):

        return (
            asset_type
            == "bigquery.googleapis.com/Dataset"
        )

    def labels(
        self,
        resource,
    ):

        dataset_info = parse_dataset_name(
            resource.name
        )

        dataset = self.client.get_dataset(
            f"{dataset_info['project']}."
            f"{dataset_info['dataset']}"
        )

        return dict(
            dataset.labels or {}
        )

    def get(
        self,
        resource_name: str,
    ) -> Resource:
        """
        Retrieves a BigQuery dataset and returns
        the platform Resource model.
        """

        dataset_info = parse_dataset_name(
            resource_name
        )

        dataset = self.client.get_dataset(
            f"{dataset_info['project']}."
            f"{dataset_info['dataset']}"
        )

        return Resource(

            asset_type="bigquery.googleapis.com/Dataset",

            name=resource_name,

            project="",

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

        dataset_info = parse_dataset_name(
            resource.name
        )

        dataset = self.client.get_dataset(
            f"{dataset_info['project']}."
            f"{dataset_info['dataset']}"
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