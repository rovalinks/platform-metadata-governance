from flask import jsonify, request

from services.executor import ExecutorService


def execute():
    """
    Execute a previously generated remediation plan.

    GET /execute?run_id=<run-id>
    """

    run_id = request.args.get(
        "run_id"
    )

    if not run_id:

        return (
            jsonify(
                {
                    "error": (
                        "Missing required "
                        "query parameter: run_id"
                    )
                }
            ),
            400,
        )

    executor = ExecutorService()

    try:

        result = executor.execute_run(
            run_id
        )

        return jsonify(result)

    except RuntimeError as error:

        return (
            jsonify(
                {
                    "error": str(error)
                }
            ),
            409,
        )