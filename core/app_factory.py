from flask import Flask

from core.config import config
from core.logger import setup_logger


def create_app(config_name="default"):

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(
        config[config_name]
    )

    setup_logger(app)

    register_routes(app)

    return app


def register_routes(app):

    try:
        from routes.system import system
        app.register_blueprint(system)

    except Exception as e:
        app.logger.error(
            f"System route error: {e}"
        )


    try:
        from dashboard.routes import dashboard
        app.register_blueprint(dashboard)

    except Exception as e:
        app.logger.warning(
            f"Dashboard route not loaded: {e}"
        )


    try:
        from routes.dashboard_v2 import dashboard_v2
        app.register_blueprint(dashboard_v2)

    except Exception as e:
        app.logger.warning(
            f"Dashboard v2 not loaded: {e}"
        )


    return app
