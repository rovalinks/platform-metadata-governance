from flask import request

from handlers.health import health
from handlers.discovery import discover
from config import PROJECT_ID


class Dispatcher:

    @staticmethod
    def dispatch():

        path = request.path

        if path == "/":
            return health()

        if path == "/health":
            return health()

        if path == "/discover":
            return discover(PROJECT_ID)

        return {
            "error": "Endpoint not found"
        }, 404