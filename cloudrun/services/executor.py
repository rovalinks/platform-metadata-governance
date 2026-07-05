from types import SimpleNamespace

from repositories.execution_repository import (
    ExecutionRepository,
)
from repositories.remediation_repository import (
    RemediationRepository,
)
from services.adapter import AdapterService
from services.task_dispatcher import (
    TaskDispatcher,
)
from utils.exceptions import format_gcp_exception
from utils.logger import logger


class ExecutorService:
    """Executes enforcement actions."""

    def __init__(self):
        self.adapters = AdapterService()
        self.repository = RemediationRepository()
        self.execution_repository = ExecutionRepository()
        self.dispatcher = TaskDispatcher()

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
                        "error": format_gcp_exception(
                            error
                        ),
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

    def execute_batch(
        self,
        run_id: str,
        offset: int,
        batch_size: int,
    ):
        """
        Execute one remediation batch.
        """

        plans = self.repository.get_planned_batch(
            run_id=run_id,
            offset=offset,
            batch_size=batch_size,
        )

        if not plans:

            return {
                "processed": 0,
                "successful": 0,
                "failed": 0,
            }

        actions = []

        for plan in plans:

            actions.append(
                {
                    "resource": plan.resource_name,
                    "asset_type": plan.asset_type,
                    "labels": plan.planned_labels,
                }
            )

        results = self.execute(actions)

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

            if result["status"] == "updated":

                successful += 1
                status = "SUCCESS"

            else:

                failed += 1
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

        logger.info(
            "Batch complete. Successful=%d Failed=%d",
            successful,
            failed,
        )

        return {
            "processed": len(plans),
            "successful": successful,
            "failed": failed,
        }

    def execute_run(
        self,
        run_id: str,
    ):
        """
        Executes remediation synchronously.
        """

        logger.info(
            "Dispatching remediation run %s",
            run_id,
        )

        if self.execution_repository.already_executed(
            run_id
        ):

            raise RuntimeError(
                f"Remediation run {run_id} has already been executed."
            )

        plans = self.repository.get_planned(
            run_id
        )

        if not plans:

            raise RuntimeError(
                f"Remediation run {run_id} was not found."
            )

        total_resources = len(
            plans
        )

        logger.info(
            "Executing remediation synchronously."
        )

        result = self.execute_batch(
            run_id=run_id,
            offset=0,
            batch_size=total_resources,
        )

        logger.info(
            "Run %s completed. Processed=%d Success=%d Failed=%d",
            run_id,
            result["processed"],
            result["successful"],
            result["failed"],
        )

        return {
            "run_id": run_id,
            "status": "COMPLETED",
            "resources": total_resources,
            "processed": result["processed"],
            "successful": result["successful"],
            "failed": result["failed"],
        }