from flask import request, jsonify

def worker():

    payload = request.get_json()

    return jsonify(payload)