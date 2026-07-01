from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

PROJECT_ID = os.environ["PROJECT_ID"]

REGISTRY_BUCKET = os.environ["REGISTRY_BUCKET"]

REGISTRY_PREFIX = "applications"