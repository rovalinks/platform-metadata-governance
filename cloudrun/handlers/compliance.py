from dataclasses import asdict

from flask import jsonify

from services.compliance import ComplianceService


service = ComplianceService()


def compliance(project_id: str):

    results = service.evaluate(project_id)

    return jsonify(
        {
            "resourceCount": len(results),
            "results": [
                asdict(result)
                for result in results
            ],
        }
    )