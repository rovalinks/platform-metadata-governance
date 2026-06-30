from models.compliance import ComplianceResult

from services.discovery import DiscoveryService
from services.governance import GovernanceService


class ComplianceService:

    def __init__(self):

        self.discovery = DiscoveryService()

        self.governance = GovernanceService()

    def evaluate(self, project_id: str):

        resources = self.discovery.discover(project_id)

        registered_products = self.governance.registered_products(project_id)

        results = []

        for resource in resources:

            registered = any(
                product.lower() in resource.name.lower()
                for product in registered_products
            )

            results.append(
                ComplianceResult(
                    asset_type=resource.asset_type,
                    name=resource.name,
                    project=resource.project,
                    registered=registered,
                )
            )

        return results