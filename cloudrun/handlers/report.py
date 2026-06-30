from flask import jsonify

from services.context import RequestContext
from services.report import ReportService

context = RequestContext()
service = ReportService(context.discovery)


def report(project_id: str):

    return jsonify(
        service.report(project_id).to_dict()
    )