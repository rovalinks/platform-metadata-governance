from repositories.execution_repository import ExecutionRepository
from repositories.run_status_repository import RunStatusRepository
from utils.logger import logger


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
        logger.info(
            "Loading status for run %s",
            run_id,
        )

        run = self.run_status.get(run_id)

        if run is None:
            logger.error(
                "Run %s not found.",
                run_id,
            )

            raise RuntimeError(
                f"Run {run_id} not found."
            )

        logger.info(
            "Run status record loaded: %s",
            run,
        )

        planned = run["planned"]

        logger.info(
            "Planned remediation actions: %d",
            planned,
        )

        execution_counts = self.execution.count_by_status(
            run_id
        )

        logger.info(
            "Execution counts: %s",
            execution_counts,
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

        logger.info(
            "Run %s summary: planned=%d processed=%d successful=%d failed=%d remaining=%d progress=%.2f%% status=%s",
            run_id,
            planned,
            processed,
            successful,
            failed,
            remaining,
            progress,
            status,
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