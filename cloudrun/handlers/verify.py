from dataclasses import asdict

from flask import jsonify

from services.verification import VerificationService


service = VerificationService()


def verify(project_id: str):

    return jsonify(
        [
            asdict(result)
            for result in service.verify(project_id)
        ]
    )