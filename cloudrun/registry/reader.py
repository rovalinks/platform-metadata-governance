from pathlib import Path

import yaml

from config import REGISTRY_DIRECTORY


class RegistryReader:
    """Reads application registry YAML files."""

    def __init__(self, registry_directory: Path = REGISTRY_DIRECTORY):
        self.registry_directory = registry_directory

    def load_all(self) -> list[dict]:

        applications = []

        for file in sorted(self.registry_directory.glob("*.yaml")):

            with file.open("r", encoding="utf-8") as stream:

                applications.append(yaml.safe_load(stream))

        return applications