from services.compliance import ComplianceService
from services.adapter import AdapterService


class EnforcementService:
    def __init__(self):
        self.compliance = ComplianceService()
        self.adapters = AdapterService()

    def plan(self, project_id: str):
        actions = []

        for result in self.compliance.evaluate(project_id):
            if result.compliant:
                continue

            client = self.adapters.client_for(result.asset_type)
            if client is None:
                continue

            actions.append(
                {
                    "resource": result.name,
                    "asset_type": result.asset_type,
                    "labels": self.compliance.governance.expected_labels(project_id),
                    "action": "apply_labels",
                }
            )

        return actions