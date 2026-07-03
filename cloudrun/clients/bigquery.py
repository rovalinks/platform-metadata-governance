from google.cloud import bigquery

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

        merged = dict(
            dataset.labels or {}
        )

        merged.update(labels)

        dataset.labels = merged

        self.client.update_dataset(
            dataset,
            ["labels"],
        )

        return True