from handlers.health import health
from handlers.discovery import discover
from handlers.compliance import compliance
from handlers.verify import verify
from handlers.report import report
from handlers.enforce import enforce


class Dispatcher:

    @staticmethod
    def dispatch(route: str):

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

        if route == "enforce":
            return enforce()

        return {
            "error": "Endpoint not found"
        }, 404