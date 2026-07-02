from datetime import datetime, timezone
from uuid import uuid4

from google.cloud import bigquery

from utils.logger import logger


class SnapshotRepository:
    """BigQuery repository for governance snapshots."""

    def __init__(self):

        self.client = bigquery.Client()

        self.dataset = "metadata_governance"

        self.inventory_table = "resource_inventory"

        self.compliance_table = "compliance_results"

    def save_inventory(self, resources):

        run_id = str(uuid4())

        snapshot_time = datetime.now(
            timezone.utc
        )

        table = (
            f"{self.client.project}."
            f"{self.dataset}."
            f"{self.inventory_table}"
        )

        rows = []

        for resource in resources:

            rows.append({

                "run_id": run_id,

                "snapshot_time": snapshot_time.isoformat(),

                "project_id": resource.project,

                "asset_type": resource.asset_type,

                "resource_name": resource.name,

                "location": resource.location,

                "labels": resource.labels,

                "tags": resource.tags,

            })

        logger.info(
            "Writing %d resources to snapshot.",
            len(rows),
        )

        errors = self.client.insert_rows_json(
            table,
            rows,
        )

        if errors:

            raise RuntimeError(errors)

        logger.info(
            "Snapshot %s written successfully.",
            run_id,
        )

        return run_id