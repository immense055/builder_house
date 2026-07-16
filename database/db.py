import pymysql


def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="builder_house",
        unix_socket="/data/data/com.termux/files/usr/var/run/mysqld.sock",
        cursorclass=pymysql.cursors.DictCursor,
    )
