from registry.reader import RegistryReader


class GovernanceService:
    """Provides access to governance metadata."""

    def __init__(self):

        self.applications = RegistryReader().load_all()

    def applications_for_project(self, project_id: str):

        matches = []

        for application in self.applications:

            for binding in application["bindings"]["gcp"]:

                if binding["projectId"] == project_id:

                    matches.append(application)

        return matches

    def registered_products(self, project_id: str):

        return {
            application["product"]
            for application in self.applications_for_project(project_id)
        }

    def governance_policy(self, product: str):

        for application in self.applications:

            if application["product"] == product:

                return application["governance"]

        return None