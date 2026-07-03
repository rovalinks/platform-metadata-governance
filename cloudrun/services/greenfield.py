from google.api_core.exceptions import NotFound

from utils.logger import logger
from utils.cloudevent_parser import CloudEventParser

from services.adapter import AdapterService
from services.classification import ClassificationService
from services.compliance import ComplianceService
from services.discovery import DiscoveryService
from services.executor import ExecutorService
from services.governance import GovernanceService


class GreenfieldService:
    """
    Handles real-time governance for newly
    created GCP resources.
    """

    def __init__(self):

        self.classification = ClassificationService()

        self.adapters = AdapterService()

        self.discovery = DiscoveryService()

        self.compliance = ComplianceService(
            self.discovery
        )

        self.governance = GovernanceService()

        self.executor = ExecutorService()

    def process(
        self,
        event: dict,
    ):

        #
        # Local testing using
        # gcloud logging read
        #
        if isinstance(
            event,
            list,
        ):
            event = event[0]

        audit_event = CloudEventParser.parse(
            event
        )

        logger.info(
            "Audit event received for %s",
            audit_event.resource_name,
        )

        resource_event = (
            self.classification.classify(
                audit_event
            )
        )

        logger.info(
            "Resource classified as %s",
            resource_event.asset_type,
        )

        client = self.adapters.client_for(
            resource_event.asset_type
        )

        if client is None:

            raise RuntimeError(
                "No adapter registered for "
                f"{resource_event.asset_type}"
            )

        try:

            resource = client.get(
                resource_event.resource_name
            )

        except NotFound:

            logger.warning(
                "Resource %s no longer exists. "
                "Skipping remediation.",
                resource_event.resource_name,
            )

            return {
                "status": "not_found",
                "resource": resource_event.resource_name,
            }

        resource.project = (
            resource_event.project_id
        )

        logger.info(
            "Resolved resource %s",
            resource.name,
        )

        compliance = (
            self.compliance.evaluate_resource(
                resource
            )
        )

        if compliance.compliant:

            logger.info(
                "Resource already compliant."
            )

            return {
                "status": "compliant",
                "resource": resource.name,
            }

        labels = (
            self.governance.expected_labels(
                resource.project
            )
        )

        logger.info(
            "Applying %d governance labels.",
            len(labels),
        )

        result = (
            self.executor.execute_resource(
                resource,
                labels,
            )
        )

        return {
            "status": "remediated",
            "resource": resource.name,
            "result": result,
        }