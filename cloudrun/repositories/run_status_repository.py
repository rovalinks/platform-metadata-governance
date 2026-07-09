from datetime import datetime

from google.cloud import bigquery

import config
from utils.logger import logger


class RunStatusRepository:
    """
    Persists and retrieves remediation run status.

    BigQuery streaming rows cannot be updated immediately,
    so this repository is append-only.
    """

    def __init__(self):
        self.client = bigquery.Client()
        self.table = (
            f"{config.BIGQUERY_DATASET}.run_status"
        )

    def create(
        self,
        run_id: str,
        project_id: str,
        planned_actions: int,
    ):
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

        errors = self.client.insert_rows_json(
            self.table,
            [row],
        )

        if errors:
            raise RuntimeError(errors)

        logger.info(
            "Created run status %s",
            run_id,
        )

    def complete(
        self,
        run_id: str,
        successful: int,
        failed: int,
    ):
        run = self.get(run_id)

        if run is None:
            raise RuntimeError(
                f"Run {run_id} not found."
            )

        row = {
            "run_id": run_id,
            "project_id": run["project_id"],
            "status": "COMPLETED",
            "planned": run["planned"],
            "successful": successful,
            "failed": failed,
            "started_at": run["started_at"],
            "completed_at": datetime.utcnow().isoformat(),
        }

        errors = self.client.insert_rows_json(
            self.table,
            [row],
        )

        if errors:
            raise RuntimeError(errors)

        logger.info(
            "Run %s marked COMPLETE",
            run_id,
        )

    def get(
        self,
        run_id: str,
    ):
        query = f"""
        SELECT *
        FROM `{self.table}`
        WHERE run_id=@run_id
        ORDER BY started_at DESC,
                 completed_at DESC
        LIMIT 1
        """

        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "run_id",
                        "STRING",
                        run_id,
                    )
                ]
            ),
        )

        for row in job.result():
            return dict(row.items())

        return None