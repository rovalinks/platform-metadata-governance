from flask import jsonify, request

from services.context import RequestContext
from services.planner import PlannerService


def plan():
    """
    Generate a remediation plan.

    GET /plan
        Generate plans for all projects in the registry.

    GET /plan?project=<project-id>
        Generate a plan for a single project.
    """

    context = RequestContext()

    service = PlannerService(
        context.discovery
    )

    project_id = request.args.get(
        "project"
    )

    result = service.create(
        project_id
    )

    return jsonify(result)