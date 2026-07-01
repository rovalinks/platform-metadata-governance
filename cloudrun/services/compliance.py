from utils.logger import logger

from models.compliance import (
    ComplianceResult,
    ComplianceSummary,
)

from services.governance import GovernanceService
from services.capability import CapabilityService


class ComplianceService:

    def __init__(self, discovery):

        self.discovery = discovery
        self.governance = GovernanceService()
        self.capability = CapabilityService()

    def compliance(self, project_id: str):
        """
        Returns both the compliance summary and detailed results.
        """

        results = self.evaluate(project_id)

        return {
            "summary": self.summary(results),
            "results": results,
        }

    def summary(self, results):
        """
        Build summary from an existing compliance result set.
        """

        total = len(results)

        compliant = sum(
            1
            for result in results
            if result.compliant
        )

        non_compliant = total - compliant

        percentage = (
            (compliant / total) * 100
            if total > 0
            else 100
        )

        return ComplianceSummary(
            total_resources=total,
            compliant_resources=compliant,
            non_compliant_resources=non_compliant,
            compliance_percentage=round(
                percentage,
                2,
            ),
        )

    def evaluate(self, project_id: str):

        logger.info(
            "Evaluating compliance for project %s",
            project_id,
        )

        resources = self.discovery.discover(project_id)

        expected_labels = (
            self.governance.expected_labels(project_id)
        )

        logger.info(
            "Expected labels: %s",
            expected_labels,
        )

        results = []

        for resource in resources:

            if not self.capability.supports_labels(
                resource.asset_type
            ):
                continue

            missing = []
            incorrect = []

            for key, expected_value in expected_labels.items():

                actual = resource.labels.get(key)

                logger.info(
                    "Resource=%s Labels=%s Key=%s Expected=%s Actual=%s",
                    resource.name,
                    resource.labels,
                    key,
                    expected_value,
                    actual,
                )

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

        logger.info(
            "Evaluated %d resources",
            len(results),
        )

        return results