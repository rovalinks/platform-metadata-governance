from datetime import datetime, timezone
# Ensure existing imports are maintained below this line if they were already present
# from your previous file (e.g., logger, etc.)

class Executor:
    # ... (other methods of the class)

    def execute_run(
        self,
        run_id: str,
    ):
        """
        Execute a previously generated remediation plan.

        Reads PLANNED remediation actions from BigQuery,
        applies the required labels using the appropriate
        resource adapter, updates execution status, and 
        returns a summary of the run.
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

        if not plans:
            raise RuntimeError(
                (
                    "Remediation run "
                    f"{run_id} "
                    "was not found."
                )
            )

        start_time = datetime.now(timezone.utc)

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

        successful = 0
        failed = 0

        for result in results:
            plan = plans_by_resource[
                result["resource"]
            ]

            status = (
                "SUCCESS"
                if result["status"] == "updated"
                else "FAILED"
            )

            if status == "SUCCESS":
                successful += 1
            else:
                failed += 1

            self.execution_repository.save(
                run_id=run_id,
                project_id=plan.project_id,
                asset_type=plan.asset_type,
                resource_name=plan.resource_name,
                status=status,
                error_message=result.get(
                    "error"
                ),
            )

        duration = (
            datetime.now(timezone.utc)
            - start_time
        ).total_seconds()

        logger.info(
            "Completed remediation run %s",
            run_id,
        )

        return {
            "run_id": run_id,
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "duration_seconds": round(
                duration,
                2,
            ),
            "results": results,
        }