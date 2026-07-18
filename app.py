from flask import Flask, request, jsonify
import bcrypt

from database.db import get_connection

from routes.auth import auth
from routes.users import users
from routes.admin import admin
from routes.bitcoin import bitcoin
from dashboard.routes import dashboard

from flask import Blueprint, jsonify
from database.db import get_connection
import secrets

from auth import require_api_key
from logger import log_request
from middleware import check_rate_limit

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(admin)
app.register_blueprint(bitcoin)
app.register_blueprint(dashboard)


@app.route("/")
def home():
    return jsonify({
        "message": "Builder House API is running"
    })


@app.route("/api-keys", methods=["GET"])
def api_keys():

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
            SELECT
                id,
                api_key,
                owner,
                plan,
                daily_limit,
                requests_today,
                last_reset,
                created_at
            FROM api_keys
            ORDER BY id DESC
            """)

            rows = cursor.fetchall()

        return jsonify(rows)

    finally:
        conn.close()


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not all([username, full_name, email, password]):
        return jsonify({
            "error": "All fields are required"
        }), 400

    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO users
                (username,full_name,email,password_hash)
                VALUES (%s,%s,%s,%s)
                """,
                (
                    username,
                    full_name,
                    email,
                    password_hash
                )
            )

        conn.commit()

        return jsonify({
            "message": "User registered successfully"
        }), 201

    finally:
        conn.close()


@app.route("/api/v1/test")
@require_api_key
def test_api():

    limit = check_rate_limit()

    if limit:
        return limit

    log_request(200)

    return jsonify({
        "status": "success",
        "message": "Builder House API Working"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
