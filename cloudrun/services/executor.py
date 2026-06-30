from utils.logger import logger 
from types import SimpleNamespace
from services.adapter import AdapterService

class ExecutorService:
    """Executes enforcement actions."""

    def __init__(self):
        self.adapters = AdapterService()

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

            client.apply_labels(
                resource,
                action["labels"],
            )

            # Log successful update
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

        return results