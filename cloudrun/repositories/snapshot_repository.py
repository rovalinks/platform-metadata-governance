import json
import os
from datetime import datetime
from google.cloud import bigquery
from utils.logger import logger

class SnapshotRepository:
    """Persists and retrieves governance snapshots."""

    def __init__(self):
        self.client = bigquery.Client()
        # Ensure this matches the dataset name exactly
        self.dataset = "metadata_governance_dataset"
        # Using resource_table to match your previous logic
        self.resource_table = "resource_snapshot"
        self.compliance_table = "compliance_snapshot"

    def save_inventory(self, resources):
        """Persists resource inventory with serialized JSON strings."""
        rows_to_insert = []
        for resource in resources:
            rows_to_insert.append({
                "run_id": resource.run_id,
                "snapshot_time": datetime.utcnow().isoformat(),
                "project_id": resource.project_id,
                "asset_type": resource.asset_type,
                "resource_name": resource.name,
                "location": resource.location,
                "labels": json.dumps(resource.labels or {}),
                "tags": json.dumps(resource.tags or {}),
            })
        
        table_id = f"{self.dataset}.{self.resource_table}"
        errors = self.client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            logger.error(f"Errors inserting resources into {table_id}: {errors}")
        return errors

    def save_compliance(self, results):
        """Persists compliance results with serialized JSON strings."""
        rows_to_insert = []
        for res in results:
            rows_to_insert.append({
                "run_id": res.run_id,
                "evaluated_time": datetime.utcnow().isoformat(),
                "project_id": res.project_id,
                "asset_type": res.asset_type,
                "resource_name": res.resource_name,
                "compliant": res.compliant,
                "missing_labels": json.dumps(res.missing_labels or []),
                "incorrect_labels": json.dumps(res.incorrect_labels or {}),
            })
            
        table_id = f"{self.dataset}.{self.compliance_table}"
        errors = self.client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            logger.error(f"Errors inserting compliance data into {table_id}: {errors}")
        return errors