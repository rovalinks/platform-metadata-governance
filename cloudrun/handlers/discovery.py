from flask import jsonify, request

from services.context import RequestContext
from services.governance import GovernanceService


context = RequestContext()

governance = GovernanceService()


def discover():
    """
    Discovers supported resources.

    Behaviour:

    GET /discover
        Discover resources across every registered project.

    GET /discover?project=<project-id>
        Discover resources for one project.
    """

    project_id = request.args.get("project")

    if project_id:

        resources = context.discovery.discover(
            project_id
        )

    else:

        resources = []

        for project in governance.projects():

            resources.extend(

                context.discovery.discover(
                    project["projectId"]
                )

            )

    return jsonify(
        [
            resource.to_dict()
            for resource in resources
        ]
    )