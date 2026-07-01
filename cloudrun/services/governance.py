from registry.reader import RegistryReader
from utils.labels import normalize_label_value
from utils.logger import logger


class GovernanceService:
    """Provides governance metadata from the registry."""

    def __init__(self):
        self.registry = RegistryReader()

    def applications_for_project(self, project_id: str):
        """
        Returns every application that contains a binding
        for the supplied GCP project.
        """

        matches = []

        for application in self.registry.load_all():

            for binding in application["bindings"]:

                if binding["cloud"] != "gcp":
                    continue

                if binding["projectId"] == project_id:
                    matches.append(application)
                    break

        return matches

    def metadata_for_project(self, project_id: str):
        """
        Returns the application metadata matching the project.
        """

        applications = self.applications_for_project(project_id)

        if not applications:
            return None

        return applications[0]

    def binding_for_project(self, application, project_id: str):
        """
        Returns the deployment binding for the project.
        """

        for binding in application["bindings"]:

            if binding["cloud"] != "gcp":
                continue

            if binding["projectId"] == project_id:
                return binding

        return None

    def expected_labels(self, project_id: str):

        logger.info(
            "Loading governance metadata for project %s",
            project_id,
        )

        application = self.metadata_for_project(project_id)

        if application is None:

            logger.warning(
                "No registry entry found for project %s",
                project_id,
            )

            return {}

        binding = self.binding_for_project(
            application,
            project_id,
        )

        if binding is None:

            logger.warning(
                "No deployment binding found for project %s",
                project_id,
            )

            return {}

        labels = {

            "application":
                normalize_label_value(application["product"]),

            "team":
                normalize_label_value(application["team"]),

            "owner":
                normalize_label_value(application["owner"]),

            "budgetowner":
                normalize_label_value(application["budgetOwner"]),

            "organization":
                normalize_label_value(application["organization"]),

            "department":
                normalize_label_value(application["department"]),

            "costcenter":
                normalize_label_value(application["costCenter"]),

            "environment":
                normalize_label_value(binding["environment"]),

            "businesscriticality":
                normalize_label_value(binding["businessCriticality"]),
        }

        logger.info(
            "Matched application '%s' for project '%s'",
            application["product"],
            project_id,
        )

        return labels