from flask import request, jsonify, g
from database.db import get_connection
from datetime import date
from middleware import check_rate_limit

def test_api():

    limit = check_rate_limit()

    if limit:
        return limit


    log_request(200)

def check_rate_limit():

    print("RATE LIMIT RUNNING")
    print("KEY:", getattr(g, "api_key", None))

    api_key = getattr(g, "api_key", None)

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    daily_limit,
                    requests_today,
                    last_reset
                FROM api_keys
                WHERE api_key=%s
                """,
                (api_key,)
            )

            data = cursor.fetchone()


            if not data:
                return jsonify({
                    "error":"API Key not found"
                }),401


            today = date.today()


            # Reset counter daily
            if str(data["last_reset"]) != str(today):

                cursor.execute(
                    """
                    UPDATE api_keys
                    SET requests_today=0,
                    last_reset=%s
                    WHERE api_key=%s
                    """,
                    (today, api_key)
                )

                conn.commit()

                used = 0

            else:
                used = data["requests_today"]



            # Limit check

            if used >= data["daily_limit"]:

                return jsonify({

                    "error":"Rate limit exceeded",

                    "limit": data["daily_limit"],

                    "used": used

                }),429



            # Increase usage

            cursor.execute(
                """
                UPDATE api_keys
                SET requests_today=requests_today+1
                WHERE api_key=%s
                """,
                (api_key,)
            )

            conn.commit()


    finally:
        conn.close()


    return None
