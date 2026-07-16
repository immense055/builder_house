from flask import Blueprint, request, jsonify
from database.db import get_connection
from utils.jwt_helper import create_token
import bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id,
                   username,
                   full_name,
                   email,
                   password_hash,
                   role,
                   status
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        if not bcrypt.checkpw(
            password.encode(),
            user["password_hash"].encode()
        ):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_token(
            user["id"],
            user["email"],
            user["role"]
        )

        user.pop("password_hash", None)

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": user
        })

    finally:
        cursor.close()
        conn.close()
