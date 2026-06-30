from models.compliance import ComplianceResult
from services.discovery import DiscoveryService
from registry.reader import RegistryReader


class ComplianceService:

    def __init__(self):
        self.discovery = DiscoveryService()
        self.registry = RegistryReader()

    def evaluate(self, project_id: str):

        resources = self.discovery.discover(project_id)

        applications = self.registry.load_all()

        registered_products = {
            application["product"]
            for application in applications
        }

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