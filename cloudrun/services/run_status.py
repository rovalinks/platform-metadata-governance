from datetime import datetime
from google.cloud import firestore
import config

class RunStatusRepository:
    """
    Handles persistence for the status and progress of remediation runs.
    """

    def __init__(self):
        self.db = firestore.Client(project=config.PROJECT_ID)
        self.collection = self.db.collection("run_status")

    def create(
        self,
        run_id: str,
        project_id: str,
        planned_actions: int,
    ):
        """
        Creates a new run status record in Firestore.
        """
        data = {
            "run_id": run_id,
            "project_id": project_id,
            "status": "QUEUED",
            "planned_actions": planned_actions,
            "successful": 0,
            "failed": 0,
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
        }

        self.collection.document(run_id).set(data)
        return data

    def complete(
        self,
        run_id: str,
        successful: int,
        failed: int,
    ):
        """
        Marks the run as completed and updates final counts.
        """
        self.collection.document(run_id).update({
            "status": "COMPLETED",
            "successful": successful,
            "failed": failed,
            "completed_at": datetime.utcnow().isoformat(),
        })

    def get_run(self, run_id: str):
        """
        Retrieves the status record for a specific run.
        """
        doc = self.collection.document(run_id).get()
        if doc.exists:
            return doc.to_dict()
        return {}