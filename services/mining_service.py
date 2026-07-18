from database.db import get_connection

def get_miners():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM miners
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data



def get_pools():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM mining_pools
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data



def get_wallets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM wallets
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data



def get_earnings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM earnings
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data



def get_mining_dashboard():

    return {
        "miners": get_miners(),
        "pools": get_pools(),
        "wallets": get_wallets(),
        "earnings": get_earnings()
    }

