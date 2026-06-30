from dataclasses import asdict

from flask import jsonify

from services.compliance import ComplianceService

from config import PROJECT_ID


service = ComplianceService()


def compliance(project_id: str):

    results = service.evaluate(project_id)

    summary = service.summary(project_id)

    return jsonify(
        {
            "summary": asdict(summary),
            "results": [
                asdict(result)
                for result in results
            ],
        }
    )