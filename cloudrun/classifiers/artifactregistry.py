from classifiers.base import ResourceClassifier
from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent


class ArtifactRegistryClassifier(ResourceClassifier):
    """Classifies Artifact Registry repository creation."""

    SERVICE = "artifactregistry.googleapis.com"

    METHOD = (
        "google.devtools.artifactregistry.v1.ArtifactRegistry.CreateRepository"
    )

    def supports(
        self,
        event: AuditLogEvent,
    ) -> bool:

        #
        # Ignore the intermediate location event:
        #
        # projects/<project>/locations/<region>
        #
        if "/repositories/" not in event.resource_name:
            return False

        return (
            event.service_name == self.SERVICE
            and event.method_name == self.METHOD
        )

    def classify(
        self,
        event: AuditLogEvent,
    ) -> ResourceEvent:

        return ResourceEvent(

            project_id=event.project_id,

            asset_type="artifactregistry.googleapis.com/Repository",

            resource_name=event.resource_name,

            service_name=event.service_name,

            method_name=event.method_name,

            location=event.location,

        )