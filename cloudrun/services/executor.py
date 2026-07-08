from types import SimpleNamespace
from concurrent.futures import ThreadPoolExecutor, as_completed

import config
from repositories.execution_repository import ExecutionRepository
from repositories.remediation_repository import RemediationRepository
from services.adapter import AdapterService
from services.cloud_task_service import CloudTaskService
from utils.exceptions import format_gcp_exception
from utils.logger import logger

class ExecutorService:
    """Executes enforcement actions."""

    def __init__(self):
        self.adapters = AdapterService()
        self.repository = RemediationRepository()
        self.execution_repository = ExecutionRepository()
        self.cloud_tasks = CloudTaskService()

    def execute(self, actions):
        """Executes enforcement actions in parallel."""
        results = []

        with ThreadPoolExecutor(
            max_workers=config.MAX_PARALLEL_WORKERS,
        ) as executor:
            # Map each action to a future
            future_to_action = {
                executor.submit(self._execute_single_action, action): action
                for action in actions
            }

            # Collect results as they complete
            for future in as_completed(future_to_action):
                results.append(future.result())

        return results

    def _execute_single_action(self, action):
        """Helper to execute a single action."""
        client = self.adapters.client_for(action["asset_type"])

        if client is None:
            return {
                "resource": action["resource"],
                "status": "unsupported",
            }

        logger.info(
            "Applying labels to %s using %s",
            action["resource"],
            client.__class__.__name__,
        )

        resource = SimpleNamespace(name=action["resource"])

        try:
            client.apply_labels(
                resource,
                action["labels"],
            )

            logger.info(
                "Successfully updated %s",
                action["resource"],
            )

            return {
                "resource": action["resource"],
                "status": "updated",
            }

        except Exception as error:
            logger.exception(
                "Failed updating %s",
                action["resource"],
            )

            return {
                "resource": action["resource"],
                "status": "failed",
                "error": format_gcp_exception(error),
            }

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

        actions = [
            {
                "resource": plan.resource_name,
                "asset_type": plan.asset_type,
                "labels": plan.planned_labels,
            }
            for plan in plans
        ]

        results = self.execute(actions)

        plans_by_resource = {
            plan.resource_name: plan
            for plan in plans
        }

        successful = 0
        failed = 0

        for result in results:
            plan = plans_by_resource[result["resource"]]

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
                error_message=result.get("error"),
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
        Enqueues the remediation run for asynchronous execution.
        """
        # Fetch planned actions count to calculate batch size
        plans = self.repository.get_planned(run_id)
        if not plans:
            raise RuntimeError(f"No planned remediation actions found for run {run_id}.")
        
        total_actions = len(plans)

        logger.info("Dispatching remediation run %s to Cloud Tasks", run_id)

        self.cloud_tasks.enqueue_remediation_batch(
            run_id=run_id,
            batch_number=1,
            total_batches=1,
            offset=0,
            batch_size=total_actions,
        )

        return {
            "run_id": run_id,
            "status": "QUEUED",
            "processed": 0,
            "successful": 0,
            "failed": 0,
        }