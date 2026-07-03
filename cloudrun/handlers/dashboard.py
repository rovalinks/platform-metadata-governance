from flask import jsonify

from services.reporting import ReportingService


def dashboard():
    """
    Returns governance dashboard KPIs.

    GET /dashboard
    """

    service = ReportingService()

    return jsonify(
        service.dashboard()
    )