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

        logger.info("========== REGISTRY READER START ==========")
        logger.info("Bucket: %s", REGISTRY_BUCKET)
        logger.info("Prefix: %s", REGISTRY_PREFIX)

        applications = []

        try:

            blobs = list(
                self.client.list_blobs(
                    REGISTRY_BUCKET,
                    prefix=REGISTRY_PREFIX,
                )
            )

            logger.info("Blob count: %d", len(blobs))

            for blob in blobs:

                logger.info("Blob: %s", blob.name)

                if not blob.name.endswith(".yaml"):
                    continue

                content = blob.download_as_text()

                applications.append(
                    yaml.safe_load(content)
                )

            logger.info("Applications loaded: %d", len(applications))

        except Exception:

            logger.exception("Failed loading registry")

            raise

        logger.info("========== REGISTRY READER END ==========")

        return applications