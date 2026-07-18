from database.db import get_connection
from flask import request, g


def log_request(status_code):

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api_logs
                (
                    api_key,
                    endpoint,
                    method,
                    ip_address,
                    status_code
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    getattr(g, "api_key", None),
                    request.path,
                    request.method,
                    request.remote_addr,
                    status_code
                )
            )

        conn.commit()

    finally:
        conn.close()

