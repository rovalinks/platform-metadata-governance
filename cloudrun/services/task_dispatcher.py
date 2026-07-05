import json

from google.cloud import tasks_v2
from google.api_core import retry

import config


class TaskDispatcher:
    """
    Creates Cloud Tasks for
    brownfield remediation.
    """

    def __init__(self):
        self.client = tasks_v2.CloudTasksClient()
        self.parent = self.client.queue_path(
            config.PROJECT_ID,
            config.REGION,
            config.TASK_QUEUE,
        )

    @retry.Retry()
    def enqueue_batch(
        self,
        run_id: str,
        batch_number: int,
        total_batches: int,
        offset: int,
        batch_size: int,
    ):
        """
        Creates a task for a specific batch in a remediation run.
        """
        payload = json.dumps(
            {
                "run_id": run_id,
                "batch_number": batch_number,
                "total_batches": total_batches,
                "offset": offset,
                "batch_size": batch_size,
            }
        ).encode()

        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                #"url": f"{config.CLOUD_RUN_URL}/worker",
                "headers": {
                    "Content-Type": "application/json"
                },
                "oidc_token": {
                    "service_account_email": config.SERVICE_ACCOUNT_EMAIL
                },
                "body": payload,
            }
        }

        return self.client.create_task(
            parent=self.parent,
            task=task,
        )