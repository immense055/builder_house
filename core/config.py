import os


class Config:

    BASE_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

    SECRET_KEY = os.environ.get(
        "BUILDER_HOUSE_SECRET",
        "builder-house-secret-key"
    )

    DEBUG = False

    DATABASE_HOST = "127.0.0.1"
    DATABASE_PORT = 3306
    DATABASE_NAME = "builder_house"
    DATABASE_USER = "root"
    DATABASE_PASSWORD = ""

    LOG_PATH = os.path.join(
        BASE_DIR,
        "logs"
    )

    MINING_PATH = os.path.join(
        BASE_DIR,
        "mining"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
} 
