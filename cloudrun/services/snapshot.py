from google.cloud import bigquery

from utils.logger import logger


class SnapshotService:
    """Persists and retrieves governance snapshots."""

    def __init__(self):

        self.client = bigquery.Client()

        self.dataset = "metadata_governance"

        self.resource_table = "resource_snapshot"

        self.compliance_table = "compliance_snapshot"

    def save_resources(self, resources):

        raise NotImplementedError

    def load_resources(self):

        raise NotImplementedError

    def save_compliance(self, results):

        raise NotImplementedError

    def load_compliance(self):

        raise NotImplementedError