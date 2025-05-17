import logging
from datetime import datetime

import pytz
from flask import has_request_context, request
from api.utils.config import config


class RequestFormatter(logging.Formatter):
    """Custom formatter to include timestamp, request IP, method, and path in logs."""

    def format(self, record):
        tz = pytz.timezone(config.TIMEZONE)
        record.timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")

        # Include request details if available
        if has_request_context():
            record.ip = (
                request.headers.get("X-Forwarded-For", request.remote_addr) or "-"
            )
            record.method = request.method
            record.path = request.path
        else:
            record.ip = "-"
            record.method = "-"
            record.path = "-"

        return super().format(record)


format = "[%(levelname)s] [%(timestamp)s] [From: %(ip)s] [%(method)s] (%(path)s): %(message)s"  # noqa: E501
formatter = RequestFormatter(format)


def setup_logger(app):
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    app.logger.setLevel(logging.getLevelName(str.upper(config.DEBUG_LEVEL)))
    app.logger.addHandler(handler)
    app.logger.propagate = False

    # Log the effective level
    current_level = logging.getLevelName(app.logger.getEffectiveLevel())
    app.logger.info(f"Starting app with DEBUG_LEVEL: {current_level}")
