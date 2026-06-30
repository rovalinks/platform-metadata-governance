from models.execution import ExecutionResult

from services.adapter import AdapterService


class ExecutorService:

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
                    ExecutionResult(
                        resource=action["resource"],
                        asset_type=action["asset_type"],
                        action=action["action"],
                        success=False,
                        message="No adapter available.",
                    )
                )

                continue

            results.append(
                ExecutionResult(
                    resource=action["resource"],
                    asset_type=action["asset_type"],
                    action=action["action"],
                    success=False,
                    message="Execution not implemented.",
                )
            )

        return results