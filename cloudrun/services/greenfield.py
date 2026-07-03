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

        # Local testing using gcloud logging read
        # returns a JSON array.
        if isinstance(
            event,
            list,
        ):
            event = event[0]

        audit_event = CloudEventParser.parse(
            event
        )

        logger.info(
            "Audit event: service=%s method=%s resource=%s",
            audit_event.service_name,
            audit_event.method_name,
            audit_event.resource_name,
        )

        resource = self.classification.classify(
            audit_event
        )

        logger.info(
            "Classification succeeded: %s",
            resource.asset_type,
        )

        return {
            "status": "classified",
            "asset_type": resource.asset_type,
            "resource": resource.resource_name,
        }