from classifiers.base import ResourceClassifier
from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent


class CloudSqlClassifier(ResourceClassifier):
    """Classifies Cloud SQL instance creation events."""

    SERVICE = "sqladmin.googleapis.com"

    METHOD = (
        "cloudsql.instances.create"
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

            asset_type="sqladmin.googleapis.com/Instance",

            resource_name=event.resource_name,

            service_name=event.service_name,

            method_name=event.method_name,

            location=event.location,

        )
