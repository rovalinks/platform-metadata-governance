from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

REGISTRY_DIRECTORY = BASE_DIR.parent / "registry" / "applications"

import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")