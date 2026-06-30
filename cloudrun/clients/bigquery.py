from google.cloud import bigquery

from clients.base import ResourceClient


class BigQueryClient(ResourceClient):
    """Applies labels to BigQuery datasets."""

    def __init__(self):

        self.client = bigquery.Client()

    def supports(self, asset_type: str):

        return asset_type == "bigquery.googleapis.com/Dataset"

    def apply_labels(self, resource, labels: dict):

        raise NotImplementedError()