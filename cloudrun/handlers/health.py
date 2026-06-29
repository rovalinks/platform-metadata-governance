from flask import jsonify

from registry.reader import RegistryReader


def health():

    applications = RegistryReader().load_all()

    return jsonify(
        {
            "service": "metadata-governance",
            "status": "healthy",
            "applications": len(applications),
            "products": [
                application["product"]
                for application in applications
            ],
        }
    )