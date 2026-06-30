from flask import jsonify

from services.context import RequestContext
from services.compliance import ComplianceService

# Initialize context and service
context = RequestContext()
service = ComplianceService(context.discovery)

def compliance(project_id: str):
    """
    Evaluates compliance for a project and returns a summary 
    and detailed results.
    """
    results = service.evaluate(project_id)
    summary = service.summary(project_id)

    return jsonify(
        {
            "summary": summary.to_dict(),
            "results": [result.to_dict() for result in results],
        }
    )