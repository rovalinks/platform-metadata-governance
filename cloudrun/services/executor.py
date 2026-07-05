from datetime import datetime, timezone
from types import SimpleNamespace

from repositories.execution_repository import (
    ExecutionRepository,
)
from repositories.remediation_repository import (
    RemediationRepository,
)
from services.adapter import AdapterService
from utils.exceptions import format_gcp_exception
from utils.logger import logger


class ExecutorService:
    """Executes enforcement actions."""

    def __init__(self):
        self.adapters = AdapterService()
        self.repository = RemediationRepository()
        self.execution_repository = ExecutionRepository()

    def execute(self, actions):
        results = []

        for action in actions:
            client = self.adapters.client_for(
                action["asset_type"]
            )

            if client is None:
                results.append(
                    {
                        "resource": action["resource"],
                        "status": "unsupported",
                    }
                )
                continue

            logger.info(
                "Applying labels to %s using %s",
                action["resource"],
                client.__class__.__name__,
            )

            resource = SimpleNamespace(
                name=action["resource"]
            )

            try:
                client.apply_labels(
                    resource,
                    action["labels"],
                )

                logger.info(
                    "Successfully updated %s",
                    action["resource"],
                )

                results.append(
                    {
                        "resource": action["resource"],
                        "status": "updated",
                    }
                )

            except Exception as error:
                logger.exception(
                    "Failed updating %s",
                    action["resource"],
                )

                results.append(
                    {
                        "resource": action["resource"],
                        "status": "failed",
                        "error": format_gcp_exception(error),
                    }
                )

        return results

    def execute_resource(
        self,
        resource,
        labels: dict,
    ):
        results = self.execute(
            [
                {
                    "resource": resource.name,
                    "asset_type": resource.asset_type,
                    "labels": labels,
                }
            ]
        )

        return results[0]

    def execute_run(
        self,
        run_id: str,
    ):
        """
        Execute a previously generated remediation plan.
        """

        if self.execution_repository.is_completed(run_id):
            logger.info(
                "Run %s already completed.",
                run_id,
            )
            return {
                "run_id": run_id,
                "total": 0,
                "successful": 0,
                "failed": 0,
                "duration_seconds": 0,
                "results": [],
            }

        logger.info(
            "Executing remediation run %s",
            run_id,
        )

        # Reset any resources that were left in an 'in-progress' state 
        # from a previous interrupted run.
        self.repository.reset_in_progress(
            run_id
        )

        successful = 0
        failed = 0
        results = []

        start_time = datetime.now(
            timezone.utc
        )

        while True:
            plans = self.repository.get_planned_batch(
                run_id
            )

            if not plans:
                break

            logger.info(
                "Processing batch of %d resources",
                len(plans),
            )

            actions = []

            for plan in plans:
                self.repository.mark_in_progress(
                    run_id,
                    plan.resource_name,
                )

                actions.append(
                    {
                        "resource": plan.resource_name,
                        "asset_type": plan.asset_type,
                        "labels": plan.planned_labels,
                    }
                )

            batch_results = self.execute(
                actions
            )

            plans_by_resource = {
                plan.resource_name: plan
                for plan in plans
            }

            for result in batch_results:
                plan = plans_by_resource[
                    result["resource"]
                ]

                if result["status"] == "updated":
                    successful += 1
                    self.repository.mark_success(
                        run_id,
                        plan.resource_name,
                    )
                    status = "SUCCESS"
                else:
                    failed += 1
                    self.repository.mark_failed(
                        run_id,
                        plan.resource_name,
                    )
                    status = "FAILED"

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

                results.append(result)

        duration = (
            datetime.now(
                timezone.utc
            )
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