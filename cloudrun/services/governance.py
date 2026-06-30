from registry.reader import RegistryReader
from utils.labels import normalize_label_value

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

        labels["application"] = normalize_label_value(application["product"])
        labels["team"] = normalize_label_value(application["team"])
        labels["owner"] = normalize_label_value(application["owner"])
        labels["budgetowner"] = normalize_label_value(application["budgetOwner"])
        labels["organization"] = normalize_label_value(application["organization"])
        labels["department"] = normalize_label_value(application["department"])
        labels["costcenter"] = normalize_label_value(application["costCenter"])
        labels["environment"] = normalize_label_value(binding["environment"])
        labels["businesscriticality"] = normalize_label_value(binding["businessCriticality"])

        return labels