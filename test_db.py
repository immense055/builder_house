from database.db import get_connection

try:
    conn = get_connection()
    print("✅ Database connected successfully!")

    with conn.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        print(cursor.fetchone())

    conn.close()

except Exception as e:
    print("❌ Error:", e)
