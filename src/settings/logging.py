# Settings for the logging system, including log levels, formatting and handlers.

import logging
import os
from pathlib import Path
from typing import Union

from settings.common import BASE_DIR


LOGS_DIR = BASE_DIR.parent / "logs"

# Create a directory if it doesn't exist
Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

LOGS_FILE_NAME = "logs"


class DebugAndInfoOnlyFilter(logging.Filter):
    """
    A logging filter that only allows DEBUG and INFO level log records to pass through.

    This filter can be added to a logger or a handler to ensure that only messages
    with a severity level of DEBUG or INFO are processed. Messages with other levels,
    such as WARNING, ERROR, or CRITICAL, will be ignored.
    """

    def filter(self, record: logging.LogRecord) -> Union[bool, logging.LogRecord]:
        """
        Determines whether the specified log record should be passed through the filter.

        Only DEBUG and INFO level records will return True; all others will return False.
        """

        return record.levelno in (logging.DEBUG, logging.INFO)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "debug_and_info_only_filter": {
            "()": DebugAndInfoOnlyFilter,
        },
    },
    "formatters": {
        "custom_formatter": {
            "format": "{levelname} - {asctime} - {pathname}:{lineno} - {funcName}() - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": [
                "debug_and_info_only_filter",
            ],
            "formatter": "custom_formatter",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "custom_formatter",
            "filename": os.path.join(LOGS_DIR, LOGS_FILE_NAME),
            "when": "midnight",
            "backupCount": 3,
        },
    },
    "root": {
        "handlers": [
            "console",
            "file",
        ],
        "level": "DEBUG",
    },
}
