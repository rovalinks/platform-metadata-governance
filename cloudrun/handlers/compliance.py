from flask import jsonify, request

from services.context import RequestContext
from services.compliance import ComplianceService


context = RequestContext()

service = ComplianceService(
    context.discovery,
)


def compliance():
    """
    Evaluates compliance.

    Behaviour:
      - GET /compliance
            Evaluate every registered GCP project.

      - GET /compliance?project=<project-id>
            Evaluate only the supplied project.
    """

    project_id = request.args.get("project")

    results = service.evaluate(project_id)

    summary = service.summary(project_id)

    return jsonify(
        {
            "summary": summary.to_dict(),
            "results": [
                result.to_dict()
                for result in results
            ],
        }
    )