from models.resource_event import ResourceEvent


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

        return ResourceEvent(

            project_id=labels.get(
                "project_id",
                "",
            ),

            asset_type=service_name,

            resource_name=resource_name,

            service_name=service_name,

            method_name=method_name,

            location=labels.get(
                "location"
            ),

        )
