from utils.logger import logger
from types import SimpleNamespace
from services.adapter import AdapterService
from utils.exceptions import format_gcp_exception
from repositories.remediation_repository import (
    RemediationRepository,
)

class ExecutorService:
    """Executes enforcement actions."""

    def __init__(self):
        self.adapters = AdapterService()
        self.repository = (
            RemediationRepository()
        )

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

            # Log the start of the specific action
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

        for result in results:

            status = (
                "SUCCESS"
                if result["status"] == "updated"
                else "FAILED"
            )

            self.repository.update_status(
                run_id=run_id,
                resource_name=result["resource"],
                status=status,
            )

        logger.info(
            "Completed remediation run %s",
            run_id,
        )

        return results