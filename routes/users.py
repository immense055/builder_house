from flask import Blueprint, request, jsonify
from utils.jwt_helper import token_required
from database.db import get_connection
import bcrypt
from utils.admin_required import admin_required

users = Blueprint("users", __name__)


@users.route("/profile", methods=["GET"])
@token_required
def profile(user_data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, full_name, email, role, status
        FROM users
        WHERE id=%s
        """,
        (user_data["user_id"],)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(user)


@users.route("/profile", methods=["PUT"])
@token_required
def update_profile(user_data):

    data = request.get_json()

    username = data.get("username")
    full_name = data.get("full_name")

    if not username or not full_name:
        return jsonify({"error": "Username and full_name are required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET username=%s,
                full_name=%s
            WHERE id=%s
            """,
            (
                username,
                full_name,
                user_data["user_id"],
            ),
        )

        conn.commit()

        return jsonify({
            "message": "Profile updated successfully"
        })

    finally:
        cursor.close()
        conn.close()


@users.route("/change-password", methods=["PUT"])
@token_required
def change_password(user_data):

    data = request.get_json()

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return jsonify({"error": "Old and new password are required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT password_hash
            FROM users
            WHERE id=%s
            """,
            (user_data["user_id"],)
        )

        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.checkpw(
            old_password.encode(),
            row["password_hash"].encode()
        ):
            return jsonify({"error": "Old password is incorrect"}), 401

        new_hash = bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute(
            """
            UPDATE users
            SET password_hash=%s
            WHERE id=%s
            """,
            (
                new_hash,
                user_data["user_id"],
            ),
        )

        conn.commit()

        return jsonify({
            "message": "Password changed successfully"
        })

    finally:
        cursor.close()
        conn.close()
@users.route("/users", methods=["GET"])
@token_required
@admin_required
def get_users(user_data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               username,
               full_name,
               email,
               role,
               status
        FROM users
        ORDER BY id
        """
    )

    users_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users_list)
