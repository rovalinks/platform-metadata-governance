from utils.logger import logger
from utils.cloudevent_parser import CloudEventParser

from services.classification import ClassificationService


class GreenfieldService:
    """
    Handles Eventarc requests.
    """

    def __init__(self):

        self.classification = (
            ClassificationService()
        )

    def process(
        self,
        event: dict,
    ):

        audit_event = (
            CloudEventParser.parse(
                event
            )
        )

        resource = (
            self.classification.classify(
                audit_event
            )
        )

        logger.info(
            "Greenfield resource classified: %s",
            resource.resource_name,
        )

        return {
            "status": "classified",
            "asset_type": resource.asset_type,
            "resource": resource.resource_name,
        }