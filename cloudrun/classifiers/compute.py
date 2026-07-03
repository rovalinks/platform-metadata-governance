from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent

from classifiers.base import ResourceClassifier


class ComputeClassifier(ResourceClassifier):
    """
    Classifies Compute Engine Audit Log events.
    """

    SERVICE = "compute.googleapis.com"

    SUPPORTED_METHODS = {
        "v1.compute.instances.insert":
            "compute.googleapis.com/Instance",

        "beta.compute.instances.insert":
            "compute.googleapis.com/Instance",

        "v1.compute.disks.insert":
            "compute.googleapis.com/Disk",

        "beta.compute.disks.insert":
            "compute.googleapis.com/Disk",
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

        asset_type = self.SUPPORTED_METHODS[
            event.method_name
        ]

        return ResourceEvent(

            project_id=event.project_id,

            asset_type=asset_type,

            resource_name=event.resource_name,

            service_name=event.service_name,

            method_name=event.method_name,

            location=event.location,

        )