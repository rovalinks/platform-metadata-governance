from models.audit_log_event import AuditLogEvent


class CloudEventParser:

    @staticmethod
    def parse(
        event: dict,
    ) -> AuditLogEvent: