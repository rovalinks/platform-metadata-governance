from abc import ABC
from abc import abstractmethod

from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent


class ResourceClassifier(ABC):
    """
    Base classifier.

    Converts one Google Audit Log event
    into one platform ResourceEvent.
    """

    @abstractmethod
    def supports(
        self,
        event: AuditLogEvent,
    ) -> bool:
        ...

    @abstractmethod
    def classify(
        self,
        event: AuditLogEvent,
    ) -> ResourceEvent:
        ...