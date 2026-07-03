from utils.logger import logger

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

        payload = event.get(
            "protoPayload",
            {}
        )

        resource = payload.get(
            "resourceName"
        )

        service = payload.get(
            "serviceName"
        )

        method = payload.get(
            "methodName"
        )

        logger.info(
            "Received Greenfield event for %s",
            resource,
        )

        return {

            "resource": resource,

            "service": service,

            "method": method,

        }