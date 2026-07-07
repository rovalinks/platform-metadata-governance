import uuid
from datetime import datetime

from google.cloud import bigquery

import config
from utils.logger import logger


class ExecutionRepository:
    """
    Persists remediation execution results.
    """

    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = config.BIGQUERY_DATASET
        self.table = "remediation_execution"

    @property
    def table_id(self):
        return f"{self.dataset}.{self.table}"

    def save(
        self,
        run_id: str,
        project_id: str,
        asset_type: str,
        resource_name: str,
        status: str,
        error_message: str | None = None,
    ):
        row = {
            "execution_id": str(uuid.uuid4()),
            "run_id": run_id,
            "project_id": project_id,
            "asset_type": asset_type,
            "resource_name": resource_name,
            "status": status,
            "error_message": (
                    str(error_message)
                    if error_message is not None
                    else None
                ),
            "executed_at": datetime.utcnow().isoformat(),
        }

        errors = self.client.insert_rows_json(
            self.table_id,
            [row],
        )

        if errors:
            logger.error(
                "Failed writing execution record: %s",
                errors,
            )
            raise RuntimeError(
                "Failed to persist execution result."
            )

        logger.info(
            "Stored execution result for %s",
            resource_name,
        )

    def already_executed(
        self,
        run_id: str,
    ) -> bool:
        """
        Returns True if this remediation run
        has already produced execution records.

        Prevents accidental re-execution of
        the same run.
        """

        query = f"""
        SELECT COUNT(*) AS total
        FROM `{self.table_id}`
        WHERE run_id = @run_id
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

        row = next(job.result())

        return row.total > 0

    def is_completed(
        self,
        run_id: str,
    ) -> bool:
        """
        Returns True only when every remediation
        action belonging to the run has completed.

        A run is considered complete when there are
        no PLANNED or IN_PROGRESS actions remaining.
        """

        query = f"""
        SELECT COUNT(*) AS total
        FROM `{config.BIGQUERY_DATASET}.remediation_plan`
        WHERE run_id = @run_id
          AND status IN (
            'PLANNED',
            'IN_PROGRESS'
          )
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

        row = next(job.result())

        return row.total == 0