from utils.logger import logger
from models.resource_event import ResourceEvent
from utils.cloudevent_parser import (
    CloudEventParser,
)

from services.governance import GovernanceService
from services.adapter import AdapterService


class GreenfieldService:
    """
    Handles real-time governance for newly
    created GCP resources.

    Triggered by Cloud Audit Log events.
    """

    def __init__(self):
        self.governance = GovernanceService()
        self.adapters = AdapterService()

    def evaluate(
        self,
        event: dict,
    ):
        """
        Parse a Cloud Audit Log event.

        Returns a normalized governance
        request for later execution.
        """
        resource = CloudEventParser.parse(
            event
        )

        logger.info(
            "Received Greenfield event for %s",
            resource.resource_name,
        )

        return resource