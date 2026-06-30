from flask import request

from handlers.health import health
from handlers.discovery import discover
from config import PROJECT_ID


class Dispatcher:

    @staticmethod
    def dispatch(route: str):

        if route == "health":
            return health()

        if route == "discover":
            return discover(PROJECT_ID)

        return {
            "error": "Endpoint not found"
        }, 404