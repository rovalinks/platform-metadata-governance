from flask import jsonify

from services.context import RequestContext
from services.enforcement import EnforcementService

context = RequestContext()
service = EnforcementService(context.discovery)


def enforce(project_id: str):
    return jsonify(
        service.execute(project_id)
    )