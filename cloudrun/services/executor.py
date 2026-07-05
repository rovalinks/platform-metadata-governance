from datetime import datetime, timezone
from math import ceil
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

    def execute_batch(
        self,
        run_id: str,
        offset: int,
        batch_size: int,
    ):
        """
        Execute a specific batch of a remediation plan.
        """
        plans = self.repository.get_planned_batch(
            run_id, offset, batch_size
        )

        if not plans:
            return

        actions = []
        for plan in plans:
            self.repository.mark_in_progress(
                run_id, plan.resource_name
            )
            actions.append(
                {
                    "resource": plan.resource_name,
                    "asset_type": plan.asset_type,
                    "labels": plan.planned_labels,
                }
            )

        batch_results = self.execute(actions)
        plans_by_resource = {
            plan.resource_name: plan for plan in plans
        }

        for result in batch_results:
            plan = plans_by_resource[result["resource"]]

            if result["status"] == "updated":
                self.repository.mark_success(
                    run_id, plan.resource_name
                )
                status = "SUCCESS"
            else:
                self.repository.mark_failed(
                    run_id, plan.resource_name
                )
                status = "FAILED"

            self.execution_repository.save(
                run_id=run_id,
                project_id=plan.project_id,
                asset_type=plan.asset_type,
                resource_name=plan.resource_name,
                status=status,
                error_message=result.get("error"),
            )

    def execute_run(
        self,
        run_id: str,
    ):
        """
        Dispatches remediation work to Cloud Tasks.

        Each Cloud Task executes one remediation batch.
        """

        logger.info(
            "Dispatching remediation run %s",
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

        batch_size = 500

        total_resources = len(plans)

        total_batches = ceil(
            total_resources / batch_size
        )

        logger.info(
            "Dispatching %d resources in %d batches",
            total_resources,
            total_batches,
        )

        for batch_number in range(
            total_batches
        ):

            offset = (
                batch_number
                * batch_size
            )

            self.dispatcher.enqueue_batch(
                run_id=run_id,
                batch_number=batch_number + 1,
                total_batches=total_batches,
                offset=offset,
                batch_size=batch_size,
            )

        logger.info(
            "Queued %d Cloud Tasks",
            total_batches,
        )

        return {
            "run_id": run_id,
            "status": "QUEUED",
            "resources": total_resources,
            "batch_size": batch_size,
            "batches": total_batches,
        }