from datetime import datetime
from google.cloud import bigquery
import config
from utils.logger import logger

class RunStatusRepository:
    """
    Persists and retrieves remediation run status using an append-only pattern.
    """

    def __init__(self):
        self.client = bigquery.Client()
        self.table = f"{config.BIGQUERY_DATASET}.run_status"

    def create(self, run_id: str, project_id: str, planned_actions: int):
        # We store the status as a new row
        row = {
            "run_id": run_id,
            "project_id": project_id,
            "status": "RUNNING",
            "planned": planned_actions,
            "successful": 0,
            "failed": 0,
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
        }

        errors = self.client.insert_rows_json(self.table, [row])
        if errors:
            raise RuntimeError(f"Failed to insert run status: {errors}")

        logger.info("Created run status %s", run_id)

    def complete(self, run_id: str, successful: int, failed: int):
        """
        Appends a 'COMPLETED' status record instead of updating existing ones.
        """
        # Fetch the original record to preserve project_id and planned count
        original_run = self.get(run_id)
        
        row = {
            "run_id": run_id,
            "project_id": original_run["project_id"],
            "status": "COMPLETED",
            "planned": original_run["planned"],
            "successful": successful,
            "failed": failed,
            "started_at": original_run["started_at"],
            "completed_at": datetime.utcnow().isoformat(),
        }

        errors = self.client.insert_rows_json(self.table, [row])
        if errors:
            raise RuntimeError(f"Failed to append completion status: {errors}")

        logger.info("Run %s marked COMPLETE via append", run_id)

    def get(self, run_id: str):
        """
        Retrieves the most recent record for a run_id using QUALIFY.
        """
        query = f"""
        SELECT *
        FROM `{self.table}`
        WHERE run_id = @run_id
        QUALIFY ROW_NUMBER() OVER(PARTITION BY run_id ORDER BY completed_at DESC, started_at DESC) = 1
        LIMIT 1
        """

        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("run_id", "STRING", run_id)
                ]
            ),
        )

        for row in job.result():
            return dict(row.items())

        return None