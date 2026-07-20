import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="network_scanner"
    )


def save_device(device):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO devices
    (ip_address, status)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
    status = VALUES(status),
    last_seen = CURRENT_TIMESTAMP
    """,
    (
        device["ip_address"],
        device["status"]
    )
)

    conn.commit()
    cursor.close()
    conn.close()
