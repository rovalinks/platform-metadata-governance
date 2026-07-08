from services.discovery import DiscoveryService
from services.compliance import ComplianceService
from services.planner import PlannerService
from services.executor import ExecutorService
from utils.logger import logger
import uuid


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

        logger.info(
            "========== BROWNFIELD START =========="
        )

        logger.info(
            "Project: %s",
            project_id,
        )

        run_id = str(uuid.uuid4())

        logger.info(
            "Governance Run ID: %s",
            run_id,
        )

        #
        # Discover
        #

        logger.info(
            "Step 1/4 - Discovering resources"
        )

        resources = self.discovery.discover(
            project_id,
            run_id,
        )

        discovered = len(resources)

        logger.info(
            "Discovery complete. %d resources discovered.",
            discovered,
        )

        #
        # Compliance
        #

        logger.info(
            "Step 2/4 - Evaluating compliance"
        )

        compliance = self.compliance.evaluate(
            project_id,
            run_id,
        )

        evaluated = len(compliance)

        logger.info(
            "Compliance complete. %d supported resources evaluated.",
            evaluated,
        )

        #
        # Plan
        #

        logger.info(
            "Step 3/4 - Generating remediation plan"
        )

        plan = self.planner.create(
            project_id,
            run_id,
        )

        logger.info(
            "Remediation plan created. Run ID: %s",
            plan["run_id"],
        )

        logger.info(
            "Planned actions: %d",
            plan["planned_actions"],
        )

        #
        # Execute
        #

        logger.info(
            "Step 4/4 - Executing remediation"
        )

        execution = self.executor.execute_run(
            plan["run_id"]
        )

        logger.info(
            "Execution complete."
        )

        logger.info(
            "Successful: %d",
            execution["successful"],
        )

        logger.info(
            "Failed: %d",
            execution["failed"],
        )

        logger.info(
            "========== BROWNFIELD COMPLETE =========="
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