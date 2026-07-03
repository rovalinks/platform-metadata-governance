def execute_run(
        self,
        run_id: str,
    ):
        """
        Execute a previously generated remediation plan.

        Reads PLANNED remediation actions from BigQuery,
        applies the required labels using the appropriate
        resource adapter, and updates execution status.
        """

        logger.info(
            "Executing remediation run %s",
            run_id,
        )

        if self.execution_repository.already_executed(
            run_id
        ):

            raise RuntimeError(
                (
                    "Remediation run "
                    f"{run_id} "
                    "has already been executed."
                )
            )

        plans = self.repository.get_planned(
            run_id
        )

        logger.info(
            "Loaded %d planned remediation actions",
            len(plans),
        )

        actions = []

        for plan in plans:

            actions.append(
                {
                    "resource": plan.resource_name,
                    "asset_type": plan.asset_type,
                    "labels": plan.planned_labels,
                }
            )

        results = self.execute(
            actions
        )

        plans_by_resource = {
            plan.resource_name: plan
            for plan in plans
        }

        for result in results:

            plan = plans_by_resource[
                result["resource"]
            ]

            self.execution_repository.save(

                run_id=run_id,

                project_id=plan.project_id,

                asset_type=plan.asset_type,

                resource_name=plan.resource_name,

                status=(
                    "SUCCESS"
                    if result["status"] == "updated"
                    else "FAILED"
                ),

                error_message=result.get(
                    "error"
                ),

            )

        logger.info(
            "Completed remediation run %s",
            run_id,
        )

        return results