from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env only for local development
load_dotenv(BASE_DIR / ".env")

#
# Google Cloud
#

PROJECT_ID = os.environ["PROJECT_ID"]

REGISTRY_BUCKET = os.environ["REGISTRY_BUCKET"]

SERVICE_ACCOUNT_EMAIL = os.getenv(
    "SERVICE_ACCOUNT_EMAIL"
)

BIGQUERY_DATASET = os.getenv(
    "BIGQUERY_DATASET",
    "metadata_governance_dataset",
)

#
# Tasks
#

TASK_QUEUE = os.getenv(
    "TASK_QUEUE"
)

REGION = os.getenv(
    "REGION"
)

CLOUD_RUN_URL = os.getenv(
    "CLOUD_RUN_URL"
)

SERVICE_ACCOUNT_EMAIL = os.getenv(
    "SERVICE_ACCOUNT_EMAIL"
)

#
# Registry
#

REGISTRY_PREFIX = "applications"

REGISTRY_CACHE_TTL = int(
    os.getenv(
        "REGISTRY_CACHE_TTL",
        "0",
    )
)

#
# Snapshot storage
#

SNAPSHOT_PREFIX = "snapshots"

RESOURCE_SNAPSHOT_PREFIX = (
    f"{SNAPSHOT_PREFIX}/inventory"
)

COMPLIANCE_SNAPSHOT_PREFIX = (
    f"{SNAPSHOT_PREFIX}/compliance"
)

#
# Discovery
#

DISCOVERY_RETENTION_DAYS = int(
    os.getenv(
        "DISCOVERY_RETENTION_DAYS",
        "10",
    )
)

#
# Enforcement
#

DRY_RUN = (
    os.getenv(
        "DRY_RUN",
        "false",
    ).lower()
    == "true"
)

#
# Logging
#

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

#
# Storage
#

EXCLUDED_BUCKETS = [
    bucket.strip()
    for bucket in os.getenv(
        "EXCLUDED_BUCKETS",
        "",
    ).split(",")
    if bucket.strip()
]

#
# Brownfield
#

PRESERVE_EXISTING_LABELS = (
    os.getenv(
        "PRESERVE_EXISTING_LABELS",
        "false",
    ).lower()
    == "false"
)

MAX_PARALLEL_WORKERS = int(
    os.getenv(
        "MAX_PARALLEL_WORKERS",
        "10",
    )
)