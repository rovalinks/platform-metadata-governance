from io import StringIO

import yaml
from google.cloud import storage

from config import REGISTRY_BUCKET, REGISTRY_PREFIX
from utils.logger import logger


class RegistryReader:
    """Reads registry YAML files from Cloud Storage."""

    def __init__(self):
        self.client = storage.Client()

    def load_all(self):

        logger.info(
            "Loading registry from bucket %s",
            REGISTRY_BUCKET,
        )

        applications = []

        blobs = self.client.list_blobs(
            REGISTRY_BUCKET,
            prefix=REGISTRY_PREFIX,
        )

        for blob in blobs:

            if not blob.name.endswith(".yaml"):
                continue

            logger.info(
                "Loading %s",
                blob.name,
            )

            content = blob.download_as_text()

            applications.append(
                yaml.safe_load(
                    StringIO(content)
                )
            )

        logger.info(
            "Loaded %d applications",
            len(applications),
        )

        return applications