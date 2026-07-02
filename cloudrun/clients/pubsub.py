from google.cloud import pubsub_v1
from google.protobuf.field_mask_pb2 import FieldMask

from clients.base import ResourceClient


class PubSubClient(ResourceClient):
    """Pub/Sub Topic adapter."""

    def __init__(self):

        self.client = pubsub_v1.PublisherClient()

    def supports(self, asset_type: str):

        return asset_type == "pubsub.googleapis.com/Topic"

    def labels(self, resource):

        topic = self.client.get_topic(
            topic=self._topic_name(resource.name)
        )

        return dict(topic.labels or {})

    def apply_labels(self, resource, labels):

        topic = self.client.get_topic(
            topic=self._topic_name(resource.name)
        )

        merged = dict(topic.labels or {})

        merged.update(labels)

        topic.labels.clear()

        topic.labels.update(merged)

        self.client.update_topic(
            topic=topic,
            update_mask=FieldMask(
                paths=["labels"]
            ),
        )

        return True

    @staticmethod
    def _topic_name(asset_name: str):

        #
        # //pubsub.googleapis.com/projects/<project>/topics/<topic>
        #

        return asset_name.replace(
            "//pubsub.googleapis.com/",
            "",
        )