from google.cloud import bigquery

from clients.base import ResourceClient
from utils.bigquery import parse_dataset_name


class BigQueryClient(ResourceClient):
    """BigQuery Dataset resource adapter."""

    def __init__(self):

        self.client = bigquery.Client()

    def supports(self, asset_type: str):

        return asset_type == "bigquery.googleapis.com/Dataset"

    def labels(self, resource):

        dataset_info = parse_dataset_name(resource.name)

        dataset = self.client.get_dataset(
            f"{dataset_info['project']}.{dataset_info['dataset']}"
        )

        return dict(dataset.labels or {})

    def apply_labels(self, resource, labels: dict):

        dataset_info = parse_dataset_name(resource.name)

        dataset = self.client.get_dataset(
            f"{dataset_info['project']}.{dataset_info['dataset']}"
        )

        merged = dict(dataset.labels or {})

        merged.update(labels)

        dataset.labels = merged

        self.client.update_dataset(
            dataset,
            ["labels"],
        )

        return True