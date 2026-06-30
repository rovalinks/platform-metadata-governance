from google.cloud import bigquery

from clients.base import ResourceClient
from utils.bigquery import parse_dataset_name


class BigQueryClient(ResourceClient):
    """Applies labels to BigQuery datasets."""

    def __init__(self):
        self.client = bigquery.Client()

    def supports(self, asset_type: str):
        return asset_type == "bigquery.googleapis.com/Dataset"

    def apply_labels(self, resource, labels: dict):

        dataset_info = parse_dataset_name(resource.name)

        dataset = self.client.get_dataset(
            f"{dataset_info['project']}.{dataset_info['dataset']}"
        )

        existing_labels = dict(dataset.labels or {})

        existing_labels.update(labels)

        dataset.labels = existing_labels

        self.client.update_dataset(
            dataset,
            ["labels"],
        )

        return True