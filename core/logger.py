import logging
import os


def setup_logger(app):

    log_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "logs"
        )
    )

    os.makedirs(
        log_dir,
        exist_ok=True
    )

    log_file = os.path.join(
        log_dir,
        "builderhouse.log"
    )

    handler = logging.FileHandler(
        log_file
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(
        formatter
    )

    app.logger.addHandler(
        handler
    )

    app.logger.setLevel(
        logging.INFO
    )

    app.logger.info(
        "Builder_House logger started"
    )
