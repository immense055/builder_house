from flask import Blueprint, jsonify
from database.db import get_connection
import secrets

api_key_routes = Blueprint("api_key_routes", __name__)

@api_key_routes.route("/api/v1/keys/create", methods=["POST"])
def create_key():

    key = "secretbh_test_" + secrets.token_hex(24)

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api_keys
                (api_key, owner, plan, daily_limit, requests_today, status, environment)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,
                (key, "Rashed", "free", 100, 0, "active", "test")
            )

        conn.commit()

        return jsonify({
            "api_key": key,
            "status": "active"
        }), 201

    finally:
        conn.close()
