from handlers.health import health
from handlers.discovery import discover
from handlers.compliance import compliance
from handlers.verify import verify
from handlers.report import report

from handlers.execute import execute
from handlers.enforce import enforce
from handlers.plan import plan

from handlers.runs import runs
from handlers.run import run
from handlers.history import history
from handlers.dashboard import dashboard
from handlers.metrics import metrics

from handlers.greenfield import greenfield


class Dispatcher:

    @staticmethod
    def dispatch(
        route: str,
        payload=None,
    ):

        if route == "health":
            return health()

        if route == "discover":
            return discover()

        if route == "compliance":
            return compliance()

        if route == "verify":
            return verify()

        if route == "report":
            return report()

        if route == "plan":
            return plan()

        if route == "execute":
            return execute()

        if route == "enforce":
            return enforce()

        #
        # Reporting
        #

        if route == "dashboard":
            return dashboard()

        if route == "runs":
            return runs()

        if route == "run":
            return run()

        if route == "history":
            return history()

        if route == "metrics":
            return metrics()

        #
        # Greenfield
        #

        if route == "greenfield":
            return greenfield(payload)

        return {
            "error": "Endpoint not found"
        }, 404