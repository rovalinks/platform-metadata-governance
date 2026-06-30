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