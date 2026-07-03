from flask import jsonify, request

from services.reporting import ReportingService


def runs():
    """
    Returns remediation runs.

    GET /runs

    GET /runs?limit=25
    """

    limit = request.args.get(
        "limit",
        default=100,
        type=int,
    )

    service = ReportingService()

    return jsonify(
        service.runs(limit)
    )