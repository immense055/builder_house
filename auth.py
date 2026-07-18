from functools import wraps
from flask import request, jsonify, g
from database.db import get_connection


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({
                "error": "Missing API Key"
            }), 401

        api_key = auth.split(" ")[1]

        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM api_keys WHERE api_key=%s",
                    (api_key,)
                )

                key = cursor.fetchone()

            if not key:
                return jsonify({
                    "error": "Invalid API Key"
                }), 401

            g.api_key = api_key

            return f(*args, **kwargs)

        finally:
            conn.close()

    return decorated
