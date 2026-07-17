import os

class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")

    # MariaDB
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "builder_house")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # API
    API_PREFIX = "/api/v1"

config = Config()
