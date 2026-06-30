from flask import jsonify

from services.context import RequestContext
from services.verification import VerificationService

context = RequestContext()
service = VerificationService(context.discovery)


def verify(project_id: str):
    return jsonify(
        [
            result.to_dict()
            for result in service.verify(project_id)
        ]
    )