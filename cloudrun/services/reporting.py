from repositories.report_repository import (
    ReportRepository,
)


class ReportingService:
    """
    Provides governance reporting.

    This service performs aggregation and
    formatting for reporting endpoints.
    """

    def __init__(self):

        self.repository = (
            ReportRepository()
        )

    def runs(
        self,
        limit: int = 100,
    ):

        return self.repository.remediation_runs(
            limit
        )

    def history(
        self,
        run_id: str,
    ):

        return self.repository.execution_history(
            run_id
        )