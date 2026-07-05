from repositories.report_repository import (
    ReportRepository,
)


class ReportingService:
    """
    Provides governance reporting.
    """

    def __init__(self):

        self.repository = (
            ReportRepository()
        )

    def dashboard(
        self,
    ):

        return self.repository.dashboard()

    def runs(
        self,
        limit: int = 100,
    ):

        return self.repository.remediation_runs(
            limit
        )

    def run(
        self,
        run_id: str,
    ):
        """
        Returns summary for a remediation run.
        """

        return self.repository.remediation_run_summary(
            run_id
        )

    def history(
        self,
        run_id: str,
    ):

        return {
            "run_id": run_id,
            "resources": self.repository.execution_history(
                run_id
            ),
        }

    def metrics(
        self,
    ):

        return self.repository.metrics()
