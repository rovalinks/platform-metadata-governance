def already_executed(
        self,
        run_id: str,
    ) -> bool:
        """
        Returns True if the remediation run
        has already been executed.
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