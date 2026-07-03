from models.audit_log_event import AuditLogEvent


class CloudEventParser:
    """
    Converts Google Cloud Audit Log events
    into the internal ResourceEvent model.
    """

    @staticmethod
    def parse(event: dict) -> ResourceEvent:

        payload = event.get(
            "protoPayload",
            {}
        )

        resource_name = payload.get(
            "resourceName",
            "",
        )

        service_name = payload.get(
            "serviceName",
            "",
        )

        method_name = payload.get(
            "methodName",
            "",
        )

        resource = event.get(
            "resource",
            {}
        )

        labels = resource.get(
            "labels",
            {}
        )

        return AuditLogEvent(

            service_name=service_name,

            method_name=method_name,

            resource_name=resource_name,

            project_id=labels.get(
                "project_id",
                "",
            ),

            location=labels.get(
                "location"
            ),
        )
