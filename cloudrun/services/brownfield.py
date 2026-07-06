from services.discovery import DiscoveryService
from services.compliance import ComplianceService
from services.planner import PlannerService
from services.executor import ExecutorService


class BrownfieldService:
    """
    Executes the complete Brownfield governance workflow.

    Discover
        ↓
    Compliance
        ↓
    Plan
        ↓
    Execute
    """

    def __init__(self):

        self.discovery = DiscoveryService()

        self.compliance = ComplianceService(
            self.discovery
        )

        self.planner = PlannerService(
            self.discovery
        )

        self.executor = ExecutorService()

    def execute(
        self,
        project_id: str,
    ):

        #
        # Discover
        #

        resources = self.discovery.discover(
            project_id
        )

        discovered = len(resources)

        #
        # Compliance
        #

        compliance = self.compliance.evaluate(
            project_id
        )

        evaluated = len(compliance)

        #
        # Plan
        #

        plan = self.planner.create(
            project_id
        )

        #
        # Execute
        #

        execution = self.executor.execute_run(
            plan["run_id"]
        )

        return {

            "project": project_id,

            "discovered": discovered,

            "evaluated": evaluated,

            "planned": plan["planned_actions"],

            "successful": execution["successful"],

            "failed": execution["failed"],

            "run_id": execution["run_id"],

            "status": execution["status"],
        }