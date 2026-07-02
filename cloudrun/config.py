from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env only if present (local development)
load_dotenv(BASE_DIR / ".env")

PROJECT_ID = os.environ["PROJECT_ID"]

REGISTRY_BUCKET = os.environ["REGISTRY_BUCKET"]

REGISTRY_PREFIX = "applications"