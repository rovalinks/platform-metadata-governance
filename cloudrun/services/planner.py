import uuid

from models.remediation import RemediationPlan
from repositories.remediation_repository import (
    RemediationRepository,
)
from services.compliance import ComplianceService
from services.governance import GovernanceService
from utils.logger import logger


class PlannerService:
    """
    Generates remediation plans for non-compliant resources.

    The planner never modifies GCP resources.
    It only creates and persists remediation plans.
    """

    def __init__(self, discovery):

        self.compliance = ComplianceService(
            discovery
        )

        self.governance = GovernanceService()

        self.repository = (
            RemediationRepository()
        )

    def create(
        self,
        project_id: str | None = None,
    ):

        logger.info(
            "Generating remediation plan"
        )

        run_id = str(
            uuid.uuid4()
        )

        results = self.compliance.evaluate(
            project_id
        )

        plans = []

        expected_labels_cache = {}

        for result in results:

            if result.compliant:
                continue

            project = result.project

            if (
                project
                not in expected_labels_cache
            ):

                expected_labels_cache[
                    project
                ] = (
                    self.governance.expected_labels(
                        project
                    )
                )

            expected_labels = (
                expected_labels_cache[
                    project
                ]
            )

            planned_labels = {}

            for label in result.missing_labels:

                if label in expected_labels:

                    planned_labels[label] = (
                        expected_labels[
                            label
                        ]
                    )

            if not planned_labels:
                continue

            plans.append(

                RemediationPlan(

                    run_id=run_id,

                    project_id=project,

                    asset_type=result.asset_type,

                    resource_name=result.name,

                    missing_labels=result.missing_labels,

                    planned_labels=planned_labels,

                )

            )

        stored = self.repository.save(
            plans
        )

        logger.info(
            "Created remediation run %s with %d planned actions",
            run_id,
            stored,
        )

        return {
            "run_id": run_id,
            "planned_actions": stored,
        }
