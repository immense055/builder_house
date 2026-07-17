from flask import request
from database.db import get_connection


def log_action(user_id, action):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get("User-Agent", "")

        cursor.execute(
            """
            INSERT INTO audit_logs
            (user_id, action, ip_address, user_agent)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, action, ip_address, user_agent),
        )

        conn.commit()

    except Exception as e:
        print("Audit Log Error:", e)

    finally:
        cursor.close()
        conn.close()
