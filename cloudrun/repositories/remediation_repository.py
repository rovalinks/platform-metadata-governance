import json

from google.cloud import bigquery

import config
from models.remediation import RemediationPlan
from utils.logger import logger


class RemediationRepository:
    """
    Persists remediation plans.

    This repository is responsible only for
    storing and retrieving remediation plans.
    """

    def __init__(self):

        self.client = bigquery.Client()

        self.dataset = config.BIGQUERY_DATASET

        self.table = "remediation_plan"

    @property
    def table_id(self):

        return (
            f"{self.dataset}.{self.table}"
        )

    def save(
        self,
        plans: list[RemediationPlan],
    ) -> int:

        if not plans:

            return 0

        rows = []

        for plan in plans:

            rows.append(

                {
                    "run_id": plan.run_id,
                    "project_id": plan.project_id,
                    "asset_type": plan.asset_type,
                    "resource_name": plan.resource_name,
                    "missing_labels": json.dumps(
                        plan.missing_labels
                    ),
                    "planned_labels": json.dumps(
                        plan.planned_labels
                    ),
                    "status": plan.status,
                    "created_at": (
                        plan.created_at.isoformat()
                    ),
                }

            )

        errors = self.client.insert_rows_json(
            self.table_id,
            rows,
        )

        if errors:

            logger.error(
                "Failed writing remediation plan: %s",
                errors,
            )

            raise RuntimeError(
                "Failed to persist remediation plan."
            )

        logger.info(
            "Stored %d remediation plans",
            len(rows),
        )

        return len(rows)