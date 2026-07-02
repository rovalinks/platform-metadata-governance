import json
import uuid
from datetime import datetime

from google.cloud import bigquery

from utils.logger import logger


class SnapshotRepository:
    """Persists and retrieves governance snapshots."""

    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = "metadata_governance_dataset"
        self.resource_table = "resource_snapshot"
        self.compliance_table = "compliance_snapshot"

    def save_inventory(self, resources):
        """Persist discovered resources to BigQuery."""

        run_id = str(uuid.uuid4())

        rows_to_insert = []

        for resource in resources:
            rows_to_insert.append(
                {
                    "run_id": run_id,
                    "snapshot_time": datetime.utcnow().isoformat(),
                    "project_id": resource.project,
                    "asset_type": resource.asset_type,
                    "resource_name": resource.name,
                    "location": resource.location,
                    "labels": json.dumps(resource.labels or {}),
                    "tags": json.dumps(resource.tags or {}),
                }
            )

        table_id = f"{self.dataset}.{self.resource_table}"

        errors = self.client.insert_rows_json(
            table_id,
            rows_to_insert,
        )

        if errors:
            logger.error(
                "Errors inserting resources into %s: %s",
                table_id,
                errors,
            )

        return run_id

    def save_compliance(self, results):
        """Persist compliance results to BigQuery."""

        rows_to_insert = []

        for res in results:
            rows_to_insert.append(
                {
                    "run_id": getattr(res, "run_id", None),
                    "evaluated_time": datetime.utcnow().isoformat(),
                    "project_id": getattr(
                        res,
                        "project_id",
                        getattr(res, "project", None),
                    ),
                    "asset_type": res.asset_type,
                    "resource_name": res.resource_name,
                    "compliant": res.compliant,
                    "missing_labels": json.dumps(
                        res.missing_labels or []
                    ),
                    "incorrect_labels": json.dumps(
                        res.incorrect_labels or {}
                    ),
                }
            )

        table_id = f"{self.dataset}.{self.compliance_table}"

        errors = self.client.insert_rows_json(
            table_id,
            rows_to_insert,
        )

        if errors:
            logger.error(
                "Errors inserting compliance data into %s: %s",
                table_id,
                errors,
            )

        return errors