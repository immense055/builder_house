from flask import request, jsonify

API_KEY = "TEST_BUILDER_HOUSE_KEY_001"

def require_api_key():

    key = request.headers.get("X-API-Key")

    if key != API_KEY:
        return jsonify({
            "error": "Invalid API Key"
        }), 401

    return None
