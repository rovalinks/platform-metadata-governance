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

            resource = SimpleNamespace(
                name=action["resource"]
            )

            client.apply_labels(
                resource,
                action["labels"],
            )

            results.append(
                {
                    "resource": action["resource"],
                    "status": "updated",
                }
            )

        return results