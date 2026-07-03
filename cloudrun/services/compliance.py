from utils.logger import logger
from models.compliance import ComplianceResult, ComplianceSummary
from services.governance import GovernanceService
from services.capability import CapabilityService


class ComplianceService:
    """Evaluates governance compliance for one or more GCP projects."""

    def __init__(self, discovery):
        self.discovery = discovery
        self.governance = GovernanceService()
        self.capability = CapabilityService()

    def evaluate(self, project_id: str | None = None):
        """
        Evaluate compliance.

        If project_id is supplied:
            - evaluate only that project

        Otherwise:
            - evaluate every GCP project registered in the registry
        """

        if project_id:

            projects = [
                {
                    "projectId": project_id,
                }
            ]

        else:

            projects = self.governance.projects()

        logger.info(
            "Evaluating compliance for %d project(s)",
            len(projects),
        )

        results = []

        for project in projects:

            results.extend(
                self._evaluate_project(
                    project["projectId"]
                )
            )

        logger.info(
            "Evaluated %d supported resources",
            len(results),
        )

        return results

    def _evaluate_project(self, project_id: str):

        logger.info(
            "Evaluating project %s",
            project_id,
        )

        resources = self.discovery.discover(project_id)

        expected_labels = self.governance.expected_labels(
            project_id
        )

        project_results = []

        for resource in resources:

            if not self.capability.supports_labels(
                resource.asset_type
            ):
                continue

            project_results.append(
                self._evaluate_resource(
                    resource,
                    expected_labels,
                )
            )

        return project_results

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

    def evaluate_resource(
        self,
        resource,
    ):
        """
        Evaluate compliance for a single
        discovered resource.
        """
        expected = self.governance.expected_labels(
            resource.project
        )

        return self._evaluate_resource(
            resource,
            expected,
        )

    def summary(self, project_id: str | None = None):

        results = self.evaluate(project_id)

        total = len(results)

        compliant = sum(
            1
            for result in results
            if result.compliant
        )

        non_compliant = total - compliant

        percentage = (
            (compliant / total) * 100
            if total
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