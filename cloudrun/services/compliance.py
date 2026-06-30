from models.compliance import ComplianceResult

from services.discovery import DiscoveryService
from services.governance import GovernanceService


class ComplianceService:

    def __init__(self):

        self.discovery = DiscoveryService()

        self.governance = GovernanceService()

    def evaluate(self, project_id: str):

        resources = self.discovery.discover(project_id)

        expected_labels = self.governance.expected_labels(project_id)

        results = []

        for resource in resources:

            missing = []

            incorrect = []

            for key, expected_value in expected_labels.items():

                actual = resource.labels.get(key)

                if actual is None:

                    missing.append(key)

                elif str(actual) != str(expected_value):

                    incorrect.append(key)

            results.append(
                ComplianceResult(
                    asset_type=resource.asset_type,
                    name=resource.name,
                    project=resource.project,
                    compliant=(
                        len(missing) == 0
                        and len(incorrect) == 0
                    ),
                    missing_labels=missing,
                    incorrect_labels=incorrect,
                )
            )

        return results