from pathlib import Path

import yaml

from config import REGISTRY_DIRECTORY
from utils.logger import logger


class RegistryReader:
    """Reads application registry YAML files."""

    def __init__(self, registry_directory: Path = REGISTRY_DIRECTORY):
        self.registry_directory = registry_directory

    def load_all(self) -> list[dict]:

        logger.info("Registry directory: %s", self.registry_directory)
        logger.info("Registry exists: %s", self.registry_directory.exists())

        files = sorted(self.registry_directory.glob("*.yaml"))

        logger.info("Registry files found: %d", len(files))

        applications = []

        for file in files:

            logger.info("Loading registry: %s", file.name)

            with file.open("r", encoding="utf-8") as stream:

                applications.append(yaml.safe_load(stream))

        logger.info("Loaded %d applications", len(applications))

        return applications