from google.cloud import bigquery

import config


class ReportRepository:
    """
    Read-only repository used for governance reporting.

    All reporting APIs read from immutable
    BigQuery tables.
    """

    def __init__(self):

        self.client = bigquery.Client()

        self.dataset = config.BIGQUERY_DATASET

    def remediation_runs(
        self,
        limit: int = 100,
    ):
        """
        Returns recent remediation runs.
        """

        query = f"""
        SELECT
            run_id,
            COUNT(*) AS planned_resources,
            MIN(created_at) AS created_at
        FROM `{self.dataset}.remediation_plan`
        GROUP BY run_id
        ORDER BY created_at DESC
        LIMIT @limit
        """

        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "limit",
                        "INT64",
                        limit,
                    )
                ]
            ),
        )

        return [
            dict(row.items())
            for row in job.result()
        ]

    def execution_history(
        self,
        run_id: str,
    ):
        """
        Returns execution history for
        one remediation run.
        """

        query = f"""
        SELECT
            execution_id,
            run_id,
            project_id,
            asset_type,
            resource_name,
            status,
            error_message,
            executed_at
        FROM `{self.dataset}.remediation_execution`
        WHERE run_id=@run_id
        ORDER BY executed_at
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

        return [
            dict(row.items())
            for row in job.result()
        ]