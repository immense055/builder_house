from flask import Blueprint, request, jsonify
from database.db import get_connection
from utils.jwt_helper import token_required
from utils.admin_required import admin_required

admin = Blueprint("admin", __name__)


@admin.route("/users", methods=["GET"])
@token_required
@admin_required
def get_users(user_data):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                id,
                username,
                full_name,
                email,
                role,
                status
            FROM users
            ORDER BY id
        """)

        users = cursor.fetchall()

        return jsonify(users), 200

    finally:
        cursor.close()
        conn.close()
@admin.route("/users/<int:user_id>", methods=["GET"])
@token_required
@admin_required
def get_user(user_data, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                username,
                full_name,
                email,
                role,
                status
            FROM users
            WHERE id=%s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user), 200

    finally:
        cursor.close()
        conn.close()
@admin.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(user_data, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE id=%s",
            (user_id,)
        )

        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute(
            "DELETE FROM users WHERE id=%s",
            (user_id,)
        )

        conn.commit()

        return jsonify({
            "message": "User deleted successfully"
        }), 200

    finally:
        cursor.close()
        conn.close()
@admin.route("/users/<int:user_id>", methods=["PUT"])
@token_required
@admin_required
def update_user(user_data, user_id):

    data = request.get_json()

    username = data.get("username")
    full_name = data.get("full_name")
    email = data.get("email")
    role = data.get("role")
    status = data.get("status")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET username=%s,
                full_name=%s,
                email=%s,
                role=%s,
                status=%s
            WHERE id=%s
            """,
            (
                username,
                full_name,
                email,
                role,
                status,
                user_id
            )
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        conn.commit()

        return jsonify({
            "message": "User updated successfully"
        }), 200

    finally:
        cursor.close()
        conn.close()
@admin.route("/users/<int:user_id>/role", methods=["PATCH"])
@token_required
@admin_required
def update_role(user_data, user_id):

    data = request.get_json()
    role = data.get("role")

    if role not in ["admin", "user"]:
        return jsonify({"error": "Invalid role"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET role=%s
            WHERE id=%s
            """,
            (role, user_id)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        conn.commit()

        return jsonify({
            "message": "Role updated successfully"
        })

    finally:
        cursor.close()
        conn.close()
@admin.route("/users/<int:user_id>/status", methods=["PATCH"])
@token_required
@admin_required
def update_status(user_data, user_id):

    data = request.get_json()
    status = data.get("status")

    if status not in ["active", "inactive", "blocked"]:
        return jsonify({"error": "Invalid status"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET status=%s
            WHERE id=%s
            """,
            (status, user_id)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        conn.commit()

        return jsonify({
            "message": "Status updated successfully"
        })

    finally:
        cursor.close()
        conn.close()
