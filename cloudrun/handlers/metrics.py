from flask import jsonify

from services.reporting import ReportingService


def metrics():
    """
    Returns remediation metrics.

    GET /metrics
    """

    service = ReportingService()

    return jsonify(
        service.metrics()
    )
