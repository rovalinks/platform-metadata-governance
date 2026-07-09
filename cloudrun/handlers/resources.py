from flask import jsonify

from services.reporting import ReportingService


def resources():

    service = ReportingService()

    return jsonify(
        service.resources()
    )