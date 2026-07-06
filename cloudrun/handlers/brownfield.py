from flask import (
    jsonify,
    request,
)

from services.brownfield import (
    BrownfieldService,
)


def brownfield():

    project = request.args.get(
        "project"
    )

    if not project:

        return (
            jsonify(
                {
                    "error": "Missing project parameter."
                }
            ),
            400,
        )

    service = BrownfieldService()

    result = service.execute(
        project
    )

    return jsonify(result)
