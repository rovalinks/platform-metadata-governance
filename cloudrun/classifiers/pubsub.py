from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent

from classifiers.base import ResourceClassifier


class PubSubClassifier(ResourceClassifier):
    """
    Classifies Pub/Sub Audit Log events.
    """

    SERVICE = "pubsub.googleapis.com"

    SUPPORTED_METHODS = {
        "google.pubsub.v1.Publisher.CreateTopic":
            "pubsub.googleapis.com/Topic",
    }

    def supports(
        self,
        event: AuditLogEvent,
    ) -> bool:

        return (
            event.service_name == self.SERVICE
            and event.method_name
            in self.SUPPORTED_METHODS
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

            location=event.location,

        )