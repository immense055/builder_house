from flask import Flask, request, jsonify
from database.db import get_connection
import bcrypt
from routes.auth import auth
from routes.users import users
from routes.admin import admin
from routes.bitcoin import bitcoin

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(admin)
app.register_blueprint(bitcoin)

@app.route("/")
def home():
    return {"message": "Builder House API is running"}


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not all([username, full_name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users
            (username, full_name, email, password_hash)
            VALUES (%s, %s, %s, %s)
            """,
            (username, full_name, email, password_hash),
        )

        conn.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000, debug=True)
