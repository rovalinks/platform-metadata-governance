from utils.logger import logger
from models.resource_event import ResourceEvent
from utils.cloudevent_parser import (
    CloudEventParser,
)

from services.audit_log import AuditLogAdapter
from services.classification import ClassificationService
from services.governance import GovernanceService
from services.execution import ExecutionService


class GreenfieldService:
    """
    Handles real-time governance for newly
    created GCP resources.

    Triggered by Cloud Audit Log events.
    """

    def __init__(self):
        self.audit = AuditLogAdapter()
        self.classification = ClassificationService()
        self.governance = GovernanceService()
        self.execution = ExecutionService()

    def process(
        self,
        event: dict,
    ):
        """
        Orchestrates the governance evaluation
        and enforcement flow.
        """
        audit_event = self.audit.parse(
            event
        )

        resource = (
            self.classification.classify(
                audit_event
            )
        )

        expected = (
            self.governance.expected_labels(
                resource.project_id
            )
        )

        # TODO
        # Read current labels
        #
        # Compare labels
        #
        # Build ExecutionRequest
        #
        # Execute if required