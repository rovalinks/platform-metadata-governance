from classifiers.base import ResourceClassifier
from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent


class PubSubClassifier(ResourceClassifier):
    """Classifies Pub/Sub Topic creation events."""

    SERVICE = "pubsub.googleapis.com"

    METHOD = (
        "google.pubsub.v1.Publisher.CreateTopic"
    )

    def supports(
        self,
        event: AuditLogEvent,
    ) -> bool:

        if (
            event.service_name
            != self.SERVICE
        ):
            return False

        if (
            event.method_name
            != self.METHOD
        ):
            return False

        #
        # Ignore Eventarc transport topics.
        #
        if (
            "/topics/eventarc-"
            in event.resource_name
        ):
            return False

        return True

    def classify(
        self,
        event: AuditLogEvent,
    ) -> ResourceEvent:

        return ResourceEvent(

            project_id=event.project_id,

            asset_type="pubsub.googleapis.com/Topic",

            resource_name=event.resource_name,

            service_name=event.service_name,

            method_name=event.method_name,

            location="global",

        )