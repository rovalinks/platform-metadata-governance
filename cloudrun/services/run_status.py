from repositories.execution_repository import ExecutionRepository
from repositories.run_status_repository import RunStatusRepository


class RunStatusService:
    """
    Returns the current status of a remediation run.
    """

    def __init__(self):
        self.run_status = RunStatusRepository()
        self.execution = ExecutionRepository()

    def get_status(
        self,
        run_id: str,
    ):
        run = self.run_status.get(run_id)

        if run is None:
            raise RuntimeError(
                f"Run {run_id} not found."
            )

        planned = run["planned"]

        execution_counts = self.execution.count_by_status(
            run_id
        )

        successful = execution_counts.get(
            "SUCCESS",
            0,
        )

        failed = execution_counts.get(
            "FAILED",
            0,
        )

        processed = successful + failed

        remaining = max(
            planned - processed,
            0,
        )

        progress = (
            round(
                (processed / planned) * 100,
                2,
            )
            if planned
            else 100
        )

        status = (
            "COMPLETED"
            if processed >= planned
            else "RUNNING"
        )

        return {
            "run_id": run_id,
            "project_id": run["project_id"],
            "planned": planned,
            "processed": processed,
            "successful": successful,
            "failed": failed,
            "remaining": remaining,
            "progress": progress,
            "status": status,
            "started_at": run["started_at"],
            "completed_at": run["completed_at"],
        }