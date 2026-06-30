from registry.reader import RegistryReader


class GovernanceService:
    """Provides application governance metadata."""

    def __init__(self):

        self.applications = RegistryReader().load_all()

    def applications_for_project(self, project_id: str):

        matches = []

        for application in self.applications:

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

        return {
            "application": application["product"],
            "team": application["team"],
            "owner": application["owner"],
            "budgetowner": application["budgetOwner"],
            "organization": application["organization"],
            "department": application["department"],
            "costcenter": application["costCenter"],
            "environment": binding["environment"],
            "businesscriticality": binding["businessCriticality"],
        }