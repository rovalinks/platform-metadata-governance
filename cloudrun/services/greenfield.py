import time
from google.api_core.exceptions import NotFound

from utils.logger import logger
from utils.cloudevent_parser import CloudEventParser

from services.adapter import AdapterService
from services.capability import CapabilityService
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
        self.compliance = ComplianceService()
        self.governance = GovernanceService()
        self.executor = ExecutorService()
        self.capability = CapabilityService()

    def process(self, event: dict):
        start = time.perf_counter()
        if isinstance(event, list):
            event = event[0]

        audit_event = CloudEventParser.parse(event)

        logger.info(
            "Greenfield Event | service=%s method=%s project=%s resource=%s",
            audit_event.service_name,
            audit_event.method_name,
            audit_event.project_id,
            audit_event.resource_name,
        )

        try:
            resource_event = self.classification.classify(audit_event)
        except ValueError as exc:
            logger.warning("Ignoring unsupported audit event. %s", exc)
            logger.info("Greenfield processing completed in %.3f seconds.", time.perf_counter() - start)
            return {
                "status": "ignored",
                "service": audit_event.service_name,
                "method": audit_event.method_name,
                "resource": audit_event.resource_name,
            }

        logger.info("Classification | asset=%s", resource_event.asset_type)

        client = self.adapters.client_for(resource_event.asset_type)

        if client is None:
            raise RuntimeError(f"No adapter registered for {resource_event.asset_type}")

        try:
            if hasattr(client, "get"):
                resource = client.get(resource_event.resource_name)
            else:
                logger.warning(
                    "Adapter for %s is missing a '.get()' method! Falling back to the slow project-wide discovery loop.",
                    resource_event.asset_type
                )
                resources = self.discovery.discover(resource_event.project_id)
                resource = next(
                    (r for r in resources if r.name == resource_event.resource_name),
                    None,
                )

            if resource is None:
                logger.warning("Resource %s no longer exists. Skipping remediation.", resource_event.resource_name)
                logger.info("Greenfield processing completed in %.3f seconds.", time.perf_counter() - start)
                return {
                    "status": "not_found",
                    "resource": resource_event.resource_name,
                }

        except NotFound:
            logger.warning("Project or resource %s no longer exists. Skipping remediation.", resource_event.resource_name)
            logger.info("Greenfield processing completed in %.3f seconds.", time.perf_counter() - start)
            return {
                "status": "not_found",
                "resource": resource_event.resource_name,
            }

        resource.project = resource_event.project_id
        logger.info("Discovery | resolved=%s", resource.name)

        if self.capability.supports_tags(resource.asset_type):
            resource.tags = self.adapters.tag_service.get_tags(resource.name)

        resources = [resource]
        logger.info("Compliance | labels=%d tags=%d", len(resource.labels), len(resource.tags))
        compliance_results = self.compliance.evaluate(resources)
        compliance = compliance_results[0]

        if compliance.compliant:
            logger.info("Resource already compliant.")
            logger.info("Greenfield processing completed in %.3f seconds.", time.perf_counter() - start)
            return {
                "status": "compliant",
                "resource": resource.name,
            }

        if self.compliance.capability.supports_labels(resource.asset_type):
            labels = self.governance.expected_labels(resource.project)
            tags = {}
            logger.info("Remediation | applying %d labels", len(labels))
        else:
            labels = {}
            tags = self.governance.expected_tags(resource.project)
            logger.info("Remediation | applying %d tags", len(tags))

        result = self.executor.execute_resource(resource, labels, tags)

        logger.info("Result | status=REMEDIATED resource=%s duration=%.3fs", resource.name, time.perf_counter() - start)
        return {
            "status": "remediated",
            "resource": resource.name,
            "result": result,
        }