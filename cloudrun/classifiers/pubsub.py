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

            asset_type="pubsub.googleapis.com/Topic",

            resource_name=event.resource_name,

            service_name=event.service_name,

            method_name=event.method_name,

            location="global",

        )