from dataclasses import asdict

from flask import jsonify

from services.report import ReportService


service = ReportService()


def report(project_id: str):

    return jsonify(
        asdict(
            service.report(project_id)
        )
    )