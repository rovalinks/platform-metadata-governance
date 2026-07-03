from collections.abc import Sequence
from typing import Optional

from classifiers.base import ResourceClassifier
from classifiers.compute import ComputeClassifier
from classifiers.storage import StorageClassifier
from models.audit_log_event import AuditLogEvent
from models.resource_event import ResourceEvent
from utils.logger import logger


class ClassificationEngine:

    def __init__(
        self,
        classifiers: Optional[Sequence[ResourceClassifier]] = None,
    ):
        self.classifiers = (
            classifiers
            if classifiers is not None
            else [
                ComputeClassifier(),
                StorageClassifier(),
            ]
        )

    def classify(
        self,
        event: AuditLogEvent,
    ) -> ResourceEvent:

        for classifier in self.classifiers:

            if classifier.supports(event):

                logger.info(
                    "Matched %s using %s",
                    event.resource_name,
                    classifier.__class__.__name__,
                )

                return classifier.classify(
                    event
                )

        raise ValueError(
            "The governance platform does not currently support this resource: "
            f"service={event.service_name}, "
            f"method={event.method_name}"
        )