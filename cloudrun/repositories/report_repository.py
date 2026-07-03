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

    def dashboard(self):
        """
        Returns governance dashboard KPIs.
        """

        query = f"""
        WITH
        resources AS (
            SELECT COUNT(*) AS total_resources
            FROM `{self.dataset}.resource_snapshot`
        ),

        compliance AS (
            SELECT
                COUNT(*) AS compliant_resources
            FROM `{self.dataset}.compliance_snapshot`
            WHERE compliant = TRUE
        ),

        non_compliance AS (
            SELECT
                COUNT(*) AS non_compliant_resources
            FROM `{self.dataset}.compliance_snapshot`
            WHERE compliant = FALSE
        ),

        plans AS (
            SELECT COUNT(*) AS planned_remediations
            FROM `{self.dataset}.remediation_plan`
        ),

        executions AS (
            SELECT
                COUNT(*) AS executed_remediations,
                COUNTIF(status = 'SUCCESS') AS successful_remediations,
                COUNTIF(status = 'FAILED') AS failed_remediations
            FROM `{self.dataset}.remediation_execution`
        )

        SELECT *
        FROM resources
        CROSS JOIN compliance
        CROSS JOIN non_compliance
        CROSS JOIN plans
        CROSS JOIN executions
        """

        row = next(self.client.query(query).result())

        total = row.total_resources
        compliant = row.compliant_resources

        percentage = (
            round((compliant / total) * 100, 2)
            if total
            else 100
        )

        success_rate = (
            round(
                (row.successful_remediations / row.executed_remediations) * 100,
                2,
            )
            if row.executed_remediations
            else 100
        )

        return {
            "total_resources": total,
            "compliant_resources": compliant,
            "non_compliant_resources": row.non_compliant_resources,
            "compliance_percentage": percentage,
            "planned_remediations": row.planned_remediations,
            "executed_remediations": row.executed_remediations,
            "successful_remediations": row.successful_remediations,
            "failed_remediations": row.failed_remediations,
            "success_rate": success_rate,
        }

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

        return [dict(row.items()) for row in job.result()]

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

        return [dict(row.items()) for row in job.result()]

    def metrics(self):
        """
        Returns remediation metrics over time.
        """

        query = f"""
        SELECT
            DATE(executed_at) AS day,
            COUNT(*) AS total,
            COUNTIF(status='SUCCESS') AS successful,
            COUNTIF(status='FAILED') AS failed
        FROM `{self.dataset}.remediation_execution`
        GROUP BY day
        ORDER BY day
        """

        job = self.client.query(query)

        return [dict(row.items()) for row in job.result()]