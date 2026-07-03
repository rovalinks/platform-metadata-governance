from utils.logger import logger
from models.resource_event import ResourceEvent
from utils.cloudevent_parser import (
    CloudEventParser,
)

from services.audit_log import AuditLogAdapter
from services.classification import ClassificationService
from services.governance import GovernanceService
from services.execution import ExecutionService
from services.adapters import AdaptersService  # Assuming this exists based on instructions


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
        self.adapters = AdaptersService()

    def process(
        self,
        event: dict,
    ):
        """
        Orchestrates the governance evaluation
        and enforcement flow.
        """
        audit_event = self.audit.parse(event)

        resource_event = self.classification.classify(
            audit_event
        )

        client = self.adapters.client_for(
            resource_event.asset_type
        )

        resource = client.get(
            resource_event.resource_name
        )

        expected = self.governance.expected_labels(
            resource.project
        )

        # TODO
        # Read current labels
        #
        # Compare labels
        #
        # Build ExecutionRequest
        #
        # Execute if required