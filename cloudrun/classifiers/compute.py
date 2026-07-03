from classifiers.base import ResourceClassifier
from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent


class ComputeClassifier(ResourceClassifier):
    """Classifies Compute Engine resource creation."""

    SERVICE = "compute.googleapis.com"

    METHODS = {

        "v1.compute.instances.insert":
            "compute.googleapis.com/Instance",

        "v1.compute.disks.insert":
            "compute.googleapis.com/Disk",

        "v1.compute.addresses.insert":
            "compute.googleapis.com/Address",

        "v1.compute.forwardingRules.insert":
            "compute.googleapis.com/ForwardingRule",

    }

    def supports(
        self,
        event: AuditLogEvent,
    ) -> bool:

        return (
            event.service_name == self.SERVICE
            and event.method_name in self.METHODS
        )

    def classify(
        self,
        event: AuditLogEvent,
    ) -> ResourceEvent:

        return ResourceEvent(

            project_id=event.project_id,

            asset_type=self.METHODS[
                event.method_name
            ],

            resource_name=event.resource_name,

            service_name=event.service_name,

            method_name=event.method_name,

            location=event.location,

        )