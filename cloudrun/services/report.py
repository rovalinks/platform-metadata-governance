from utils.logger import logger
from models.report import GovernanceReport
from services.discovery import DiscoveryService
from services.compliance import ComplianceService
from services.enforcement import EnforcementService

class ReportService:

    def __init__(self, discovery):
        self.discovery = discovery
        self.compliance = ComplianceService(discovery)
        self.enforcement = EnforcementService(discovery)

    def report(self, project_id: str):
        logger.info("Generating governance report")

        resources = self.discovery.discover(project_id)
        compliance = self.compliance.evaluate(project_id)
        actions = self.enforcement.plan(project_id)

        compliant = sum(
            1 for item in compliance
            if item.compliant
        )

        return GovernanceReport(
            project=project_id,
            total_resources=len(resources),
            supported_resources=len(compliance),
            compliant_resources=compliant,
            non_compliant_resources=len(compliance) - compliant,
            enforcement_candidates=len(actions),
            compliance_percentage=(
                round(
                    compliant / len(compliance) * 100,
                    2,
                )
                if compliance
                else 100.0
            ),
        )