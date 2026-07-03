from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent

from classifiers.base import ResourceClassifier


class StorageClassifier(ResourceClassifier):
    """
    Classifies Cloud Storage Audit Log events.
    """

    SERVICE = "storage.googleapis.com"

    SUPPORTED_METHODS = {
        "storage.buckets.create":
            "storage.googleapis.com/Bucket",
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

            asset_type="storage.googleapis.com/Bucket",

            resource_name=event.resource_name,

            service_name=event.service_name,

            method_name=event.method_name,

            location=event.location,

        )