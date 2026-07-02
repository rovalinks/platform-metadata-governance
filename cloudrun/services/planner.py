from services.compliance import ComplianceService
from services.governance import GovernanceService
from repositories.remediation_repository import (
    RemediationRepository,
)
from models.remediation import RemediationPlan
from utils.logger import logger

import uuid


class PlannerService:
    """
    Generates remediation plans from compliance results.
    """

    def __init__(
        self,
        discovery,
    ):

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

        if project_id:

            projects = [
                {
                    "projectId": project_id,
                }
            ]

        else:

            projects = self.governance.projects()

        total_actions = 0

        remediation_run = str(
            uuid.uuid4()
        )

        for project in projects:

            pid = project["projectId"]

            expected_labels = (
                self.governance.expected_labels(
                    pid
                )
            )

            compliance_results = (
                self.compliance.evaluate(
                    pid
                )
            )

            plans = []

            for result in compliance_results:

                if result.compliant:
                    continue

                labels = {}

                for label in result.missing_labels:

                    if label in expected_labels:

                        labels[label] = (
                            expected_labels[
                                label
                            ]
                        )

                if not labels:
                    continue

                plans.append(

                    RemediationPlan(

                        run_id=remediation_run,

                        project_id=pid,

                        asset_type=result.asset_type,

                        resource_name=result.name,

                        missing_labels=result.missing_labels,

                        planned_labels=labels,

                    )

                )

            if plans:

                self.repository.save(
                    plans
                )

            total_actions += len(
                plans
            )

        logger.info(

            "Generated remediation run %s with %d actions",

            remediation_run,

            total_actions,

        )

        return {

            "run_id": remediation_run,

            "planned_actions": total_actions,

        }