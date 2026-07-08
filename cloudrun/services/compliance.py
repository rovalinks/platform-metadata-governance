from utils.logger import logger
from models.compliance import ComplianceResult, ComplianceSummary
from services.governance import GovernanceService
from services.capability import CapabilityService


class ComplianceService:
    """Evaluates governance compliance for one or more GCP resources."""

    def __init__(self):
        self.governance = GovernanceService()
        self.capability = CapabilityService()

    def evaluate(self, resources, run_id: str | None = None):
        """
        Evaluate compliance for a provided list of resources.
        """
        logger.info(
            "Evaluating compliance for %d resource(s)",
            len(resources),
        )

        results = []
        expected_cache = {}  # Cache for governance labels

        for resource in resources:
            # Check if resource type is supported for label evaluation
            if not self.capability.supports_labels(resource.asset_type):
                continue

            # Fetch expected labels for the specific project, using cache
            project = resource.project
            if project not in expected_cache:
                expected_cache[project] = self.governance.expected_labels(project)
            expected_labels = expected_cache[project]

            # Evaluate resource
            results.append(
                self._evaluate_resource(
                    resource,
                    expected_labels,
                )
            )

        logger.info(
            "Evaluated %d supported resources",
            len(results),
        )

        if run_id:
            from repositories.snapshot_repository import SnapshotRepository

            SnapshotRepository().save_compliance(
                results,
                run_id,
            )

        return results

    def _evaluate_resource(
        self,
        resource,
        expected_labels,
    ):
        """Helper to evaluate compliance for a single resource."""
        missing = []
        incorrect = []

        for key, expected in expected_labels.items():
            actual = resource.labels.get(key)

            if actual is None:
                missing.append(key)
            elif str(actual) != str(expected):
                incorrect.append(key)

        return ComplianceResult(
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

    def evaluate_resource(self, resource):
        """
        Evaluate compliance for a single discovered resource.
        """
        expected = self.governance.expected_labels(resource.project)
        return self._evaluate_resource(resource, expected)

    def summary(self, resources):
        """
        Generate a summary for a provided list of resources.
        """
        results = self.evaluate(resources)
        total = len(results)
        
        compliant = sum(1 for result in results if result.compliant)
        non_compliant = total - compliant
        percentage = ((compliant / total) * 100) if total else 100

        return ComplianceSummary(
            total_resources=total,
            compliant_resources=compliant,
            non_compliant_resources=non_compliant,
            compliance_percentage=round(percentage, 2),
        )