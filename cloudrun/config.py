from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

REGISTRY_DIRECTORY = BASE_DIR.parent / "registry" / "applications"

PROJECT_ID = os.environ["PROJECT_ID"]