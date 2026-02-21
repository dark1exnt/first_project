import os
import sys

from loguru import logger


def setup_logging():
    env = os.getenv("APP_ENV", "dev")
    level = os.getenv("LOG_LEVEL", "INFO")
    log_to_file = os.getenv("LOG_TO_FILE", "1") == "1"

    logger.remove()

    if env == "prod":
        logger.add(sys.stdout, level=level, serialize=True, enqueue=True)
    else:
        fmt = "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
        logger.add(sys.stdout, level=level, format=fmt)

    if log_to_file:
        logger.add("logs/app.log", rotation="10 MB", retention="7 days", compression="zip")

    return logger
