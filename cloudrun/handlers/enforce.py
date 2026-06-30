from flask import jsonify

from services.enforcement import EnforcementService


service = EnforcementService()


def enforce(project_id: str):
    return jsonify(
        service.execute(project_id)
    )