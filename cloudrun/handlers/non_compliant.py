from flask import jsonify

from services.reporting import ReportingService


def non_compliant():

    service = ReportingService()

    return jsonify(
        service.non_compliant()
    )