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

    def resources(self, limit: int = 100):
        """
        Returns a list of resources from the snapshot.
        """
        query = f"""
        SELECT
            project_id,
            asset_type,
            resource_name,
            location,
            labels
        FROM `{self.dataset}.resource_snapshot`
        ORDER BY project_id, asset_type
        LIMIT @limit
        """
        
        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("limit", "INT64", limit)
                ]
            ),
        )
        
        return [dict(row.items()) for row in job.result()]

    def non_compliant(self, limit: int = 100):
        """
        Returns a list of resources that still need remediation.
        """
        query = f"""
        SELECT
            project_id,
            asset_type,
            resource_name
        FROM `{self.dataset}.compliance_snapshot`
        WHERE compliant = FALSE
        ORDER BY asset_type, resource_name
        LIMIT @limit
        """

        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("limit", "INT64", limit)
                ]
            ),
        )

        return [dict(row.items()) for row in job.result()]

    def dashboard(self):
        """
        Returns governance dashboard KPIs, project counts, resource type breakdown, 
        top non-compliant resources, and recent remediation runs.
        """

        # 1. Summary Query
        summary_query = f"""
        WITH
        resources AS (
            SELECT 
                COUNT(*) AS total_resources,
                COUNT(DISTINCT project_id) AS total_projects
            FROM `{self.dataset}.resource_snapshot`
        ),
        compliance AS (
            SELECT 
                COUNT(*) AS supported_resources,
                COUNTIF(compliant = TRUE) AS compliant_resources,
                COUNTIF(compliant = FALSE) AS non_compliant_resources
            FROM `{self.dataset}.compliance_snapshot`
        ),
        plans AS (
            SELECT 
                COUNT(*) AS planned_remediations
            FROM `{self.dataset}.remediation_plan`
        ),
        executions AS (
            SELECT
                COUNT(*) AS executed_remediations,
                COUNTIF(status = 'SUCCESS') AS successful_remediations,
                COUNTIF(status = 'FAILED') AS failed_remediations,
                COUNTIF(status = 'IN_PROGRESS') AS in_progress_remediations
            FROM `{self.dataset}.remediation_execution`
        )
        SELECT *
        FROM resources
        CROSS JOIN compliance
        CROSS JOIN plans
        CROSS JOIN executions
        """

        row = next(self.client.query(summary_query).result())

        summary = {
            "projects": row.total_projects,
            "total_resources": row.total_resources,
            "supported_resources": row.supported_resources,
            "compliant_resources": row.compliant_resources,
            "non_compliant_resources": row.non_compliant_resources,
            "compliance_percentage": round((row.compliant_resources / row.supported_resources) * 100, 2) 
                                     if row.supported_resources > 0 else 100,
            "planned_remediations": row.planned_remediations,
            "remaining_remediations": (
                row.planned_remediations
                - row.executed_remediations
            ),
            "in_progress_remediations": row.in_progress_remediations,
            "executed_remediations": row.executed_remediations,
            "successful_remediations": row.successful_remediations,
            "failed_remediations": row.failed_remediations,
            "success_rate": round((row.successful_remediations / row.executed_remediations) * 100, 2) 
                       if row.executed_remediations > 0 else 100,
        }

        # 2. Compliance breakdown
        resource_types = self.compliance_breakdown()

        # 3. Top 10 Non-Compliant Resources
        non_compliant_query = f"""
        SELECT
            project_id,
            asset_type,
            resource_name,
            missing_labels,
            incorrect_labels
        FROM `{self.dataset}.compliance_snapshot`
        WHERE compliant = FALSE
        LIMIT 10
        """
        top_non_compliant = [dict(row.items()) for row in self.client.query(non_compliant_query).result()]

        # 4. Recent remediation runs
        recent_runs = self.remediation_runs(5)

        # 5. Final return
        return {
            "summary": summary,
            "resource_types": resource_types,
            "top_non_compliant": top_non_compliant,
            "recent_runs": recent_runs,
        }

    def compliance_breakdown(self):
        """
        Returns compliance grouped by resource type.
        """
        query = f"""
        SELECT
            asset_type,
            COUNT(*) AS total,
            COUNTIF(compliant) AS compliant,
            COUNTIF(NOT compliant) AS non_compliant
        FROM `{self.dataset}.compliance_snapshot`
        GROUP BY asset_type
        ORDER BY total DESC
        """

        results = []
        for row in self.client.query(query).result():
            total = row.total
            results.append({
                "asset_type": row.asset_type,
                "total": total,
                "compliant": row.compliant,
                "non_compliant": row.non_compliant,
                "compliance_percentage": round(row.compliant * 100 / total, 2)
                                       if total > 0 else 100,
            })
        return results

    def remediation_runs(self, limit: int = 100):
        """
        Returns recent remediation runs with summary metrics.
        Joins remediation_plan (planned) with remediation_execution (status).
        """
        query = f"""
        WITH plan_counts AS (
            SELECT run_id, COUNT(*) AS planned_total, MIN(created_at) AS started
            FROM `{self.dataset}.remediation_plan`
            GROUP BY run_id
        ),
        exec_counts AS (
            SELECT 
                run_id,
                COUNTIF(status='SUCCESS') AS completed,
                COUNTIF(status='FAILED') AS failed,
                COUNTIF(status='IN_PROGRESS') AS in_progress
            FROM `{self.dataset}.remediation_execution`
            GROUP BY run_id
        )
        SELECT 
            p.run_id,
            p.planned_total AS planned,
            COALESCE(e.completed, 0) AS completed,
            COALESCE(e.failed, 0) AS failed,
            COALESCE(e.in_progress, 0) AS in_progress,
            (p.planned_total - COALESCE(e.completed, 0) - COALESCE(e.failed, 0) - COALESCE(e.in_progress, 0)) AS remaining,
            p.started
        FROM plan_counts p
        LEFT JOIN exec_counts e ON p.run_id = e.run_id
        ORDER BY p.started DESC
        LIMIT @limit
        """

        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("limit", "INT64", limit)]
            ),
        )

        results = []
        for row in job.result():
            data = dict(row.items())
            total = data['planned']
            data['success_rate'] = (
                round((data['completed'] / total) * 100, 2) if total > 0 else 100.0
            )
            results.append(data)

        return results

    def remediation_run_summary(self, run_id: str):
        """
        Returns a complete summary for a remediation run.
        """
        query = f"""
        WITH
        planned AS (
            SELECT
                run_id,
                COUNT(*) AS planned,
                MIN(created_at) AS started
            FROM `{self.dataset}.remediation_plan`
            WHERE run_id=@run_id
            GROUP BY run_id
        ),
        execution AS (
            SELECT
                run_id,
                COUNTIF(status='SUCCESS') AS completed,
                COUNTIF(status='FAILED') AS failed,
                COUNTIF(status='IN_PROGRESS') AS in_progress,
                MAX(executed_at) AS finished
            FROM `{self.dataset}.remediation_execution`
            WHERE run_id=@run_id
            GROUP BY run_id
        )
        SELECT 
            p.planned,
            e.completed,
            e.failed,
            e.in_progress,
            p.started,
            e.finished
        FROM planned p
        LEFT JOIN execution e ON p.run_id = e.run_id
        """

        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("run_id", "STRING", run_id)]
            ),
        )

        row = next(job.result())
        total = row.planned
        completed = row.completed or 0
        failed = row.failed or 0
        in_progress = row.in_progress or 0

        return {
            "run_id": run_id,
            "planned": total,
            "completed": completed,
            "failed": failed,
            "remaining": total - (completed + failed + in_progress),
            "in_progress": in_progress,
            "success_rate": round(completed * 100 / total, 2) if total else 100,
            "started": row.started,
            "finished": row.finished,
        }

    def execution_history(self, run_id: str):
        """
        Returns execution history for one remediation run.
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
                query_parameters=[bigquery.ScalarQueryParameter("run_id", "STRING", run_id)]
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