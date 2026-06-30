from flask import request

from handlers.health import health
from handlers.discovery import discover
from handlers.compliance import compliance
from handlers.enforce import enforce
from handlers.verify import verify
from config import PROJECT_ID


class Dispatcher:

    @staticmethod
    def dispatch(route: str):

        if route == "health":
            return health()

        if route == "discover":
            return discover(PROJECT_ID)
        
        if route == "compliance":
            return compliance(PROJECT_ID)

        if route == "enforce":
            return enforce(PROJECT_ID)

        if route == "verify":
            return verify(PROJECT_ID)

        return {
            "error": "Endpoint not found"
        }, 404