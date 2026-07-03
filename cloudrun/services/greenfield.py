from utils.logger import logger
from utils.cloudevent_parser import CloudEventParser

from services.classification import ClassificationService
from services.adapter import AdapterService


class GreenfieldService:
    """
    Handles Eventarc requests.
    """

    def __init__(self):

        self.classification = ClassificationService()
        self.adapters = AdapterService()

    def process(
        self,
        event: dict,
    ):

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

        resource_event = self.classification.classify(
            audit_event
        )

        logger.info(
            "Classification succeeded: %s",
            resource_event.asset_type,
        )

        client = self.adapters.client_for(
            resource_event.asset_type
        )

        if client is None:

            raise RuntimeError(
                f"No adapter found for "
                f"{resource_event.asset_type}"
            )

        logger.info(
            "Resolving resource using %s",
            client.__class__.__name__,
        )

        resource = client.get(
            resource_event.resource_name
        )

        logger.info(
            "Resolved resource %s",
            resource.name,
        )

        return {
            "status": "resolved",
            "resource": resource.name,
        }