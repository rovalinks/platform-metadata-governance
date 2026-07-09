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
        # Restored to act as a safe fallback to prevent 500 errors
        self.discovery = DiscoveryService()
        self.compliance = ComplianceService()
        self.governance = GovernanceService()
        self.executor = ExecutorService()

    def process(
        self,
        event: dict,
    ):
        if isinstance(event, list):
            event = event[0]

        audit_event = CloudEventParser.parse(event)

        logger.info(
            "Audit event received for %s",
            audit_event.resource_name,
        )

        resource_event = self.classification.classify(audit_event)

        if resource_event is None:
            logger.info("Ignoring unsupported audit event.")
            return {"status": "ignored"}

        logger.info(
            "Resource classified as %s",
            resource_event.asset_type,
        )

        client = self.adapters.client_for(resource_event.asset_type)

        if client is None:
            raise RuntimeError(
                "No adapter registered for "
                f"{resource_event.asset_type}"
            )

        try:
            # Bulletproof fetch: Tries O(1) get() first, falls back to the discovery loop if the adapter is missing the method.
            if hasattr(client, "get"):
                resource = client.get(resource_event.resource_name)
            else:
                logger.warning(
                    "Adapter for %s is missing a '.get()' method! "
                    "Falling back to the slow project-wide discovery loop.",
                    resource_event.asset_type
                )
                resources = self.discovery.discover(resource_event.project_id)
                resource = next(
                    (r for r in resources if r.name == resource_event.resource_name),
                    None,
                )

            if resource is None:
                logger.warning(
                    "Resource %s no longer exists. "
                    "Skipping remediation.",
                    resource_event.resource_name,
                )
                return {
                    "status": "not_found",
                    "resource": resource_event.resource_name,
                }
                
        except NotFound:
            logger.warning(
                "Project or resource %s no longer exists. "
                "Skipping remediation.",
                resource_event.resource_name,
            )
            return {
                "status": "not_found",
                "resource": resource_event.resource_name,
            }

        resource.project = resource_event.project_id

        logger.info(
            "Resolved resource %s",
            resource.name,
        )

        # Evaluate only the single triggered resource
        resources = [resource]
        compliance_results = self.compliance.evaluate(resources)
        compliance = compliance_results[0]

        if compliance.compliant:
            logger.info("Resource already compliant.")
            return {
                "status": "compliant",
                "resource": resource.name,
            }

        labels = self.governance.expected_labels(resource.project)

        logger.info(
            "Applying %d governance labels.",
            len(labels),
        )

        result = self.executor.execute_resource(
            resource,
            labels,
        )

        return {
            "status": "remediated",
            "resource": resource.name,
            "result": result,
        }