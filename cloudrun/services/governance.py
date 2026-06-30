from registry.reader import RegistryReader


class GovernanceService:
    """Provides governance metadata from the registry."""

    def __init__(self):

        self.registry = RegistryReader()

    def applications_for_project(self, project_id: str):

        matches = []

        for application in self.registry.load_all():

            for binding in application["bindings"]["gcp"]:

                if binding["projectId"] == project_id:

                    matches.append(application)

        return matches

    def metadata_for_project(self, project_id: str):

        applications = self.applications_for_project(project_id)

        if not applications:

            return None

        return applications[0]

    def expected_labels(self, project_id: str):

        application = self.metadata_for_project(project_id)

        if application is None:

            return {}

        binding = application["bindings"]["gcp"][0]

        labels = {}

        labels["application"] = application["product"]
        labels["team"] = application["team"]
        labels["owner"] = application["owner"]
        labels["budgetowner"] = application["budgetOwner"]
        labels["organization"] = application["organization"]
        labels["department"] = application["department"]
        labels["costcenter"] = application["costCenter"]
        labels["environment"] = binding["environment"]
        labels["businesscriticality"] = binding["businessCriticality"]

        return labels