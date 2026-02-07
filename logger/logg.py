import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger


def custom_logger(
        logger_name: str = "fLogger",
        log_dir: str = "./application_logs/",
        log_filename: str = "screenshots.log",
):
    # Create logger
    logger = logging.getLogger(logger_name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    log_file_path = os.path.join(log_dir, log_filename)

    # Rotating log handler (midnight rotation)
    file_handler = TimedRotatingFileHandler(
        filename=log_file_path,
        backupCount=30,
        when="midnight",
        interval=1,
        encoding="utf-8",
        utc=False
    )

    # Keep .log extension
    file_handler.namer = lambda name: name.replace(".log", "") + ".log"

    # JSON formatter (structured logs)
    json_format = (
        "%(asctime)s %(levelname)s %(name)s %(filename)s %(funcName)s "
        "%(lineno)d %(message)s"
    )
    json_formatter = jsonlogger.JsonFormatter(json_format)

    file_handler.setFormatter(json_formatter)

    # Console handler (JSON logs to stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(json_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Prevent duplicate logging in root logger
    logger.propagate = False

    return logger


# global logger
log = custom_logger()
