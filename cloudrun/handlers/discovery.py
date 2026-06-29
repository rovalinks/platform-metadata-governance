from flask import jsonify

from services.discovery import DiscoveryService
from dataclasses import asdict


service = DiscoveryService()


def discover(project_id: str):

    resources = service.discover(project_id)

    return jsonify(
        {
            "resourceCount": len(resources),
            "resources": [asdict(resource) for resource in resources],
        }
    )