from flask import jsonify, request

from services.context import RequestContext
from services.governance import GovernanceService
from services.verification import VerificationService


context = RequestContext()

governance = GovernanceService()

service = VerificationService(context.discovery)


def verify():
    """
    Verify label compliance.

    GET /verify
        Verify every registered project.

    GET /verify?project=<project-id>
        Verify one project.
    """

    project_id = request.args.get("project")

    if project_id:

        results = service.verify(project_id)

    else:

        results = []

        for project in governance.projects():

            results.extend(

                service.verify(
                    project["projectId"]
                )

            )

    return jsonify(

        [

            result.to_dict()

            for result in results

        ]

    )