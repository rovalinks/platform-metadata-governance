from flask import jsonify
from services.reporting import ReportingService

def compliance():
    service = ReportingService()
    return jsonify(service.compliance())