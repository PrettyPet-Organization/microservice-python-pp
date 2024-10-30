import inspect
import logging.config
from typing import (
    Any,
    Optional,
)

from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import check_method


class CheckSystem(APIView):
    """
    Class for checking system settings and their status.

    Inherits from `APIView` and provides methods for performing checks, such as logging configuration.
    Uses a decorator to execute checks and handle error and success messages.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        The CheckSystem constructor.

        Sets default values for error and success messages and initializes an empty dictionary for storing
        data.
        """

        super().__init__(**kwargs)
        self.DEFAULT_ERROR_MESSAGE = _("Check {item} failed.")
        self.DEFAULT_SUCCESS_MESSAGE = _("Successfully configured!")
        self.data: dict[str, Any] = {}

    @check_method(
        data_item_name="logs",
        error_message=_("Logging is not configured in the project."),
        success_message=_("Logging is working!"),
    )
    def check_logs(self) -> Optional[bool]:
        """
        Checks the logging configuration.

        Processes examples of logs of different levels. Initializes the logger based on the settings.LOGGING
        configuration and processes logs of various levels: DEBUG, INFO, WARNING, ERROR, and CRITICAL. Handles
        exceptions that may occur during the setup.

        :return: True if logging is configured correctly, False otherwise.

        :raises ImportError: If the logging.config module could not be imported.
        :raises KeyError: If a required key is missing from the logging configuration.
        :raises Exception: To handle any other exceptions that may occur during setting up or using logging.
        """

        try:
            logger = logging.getLogger(__name__)

            logger.debug("example DEBUG message")
            logger.info("example INFO message")
            logger.warning("example WARNING message")
            logger.error("example ERROR message")
            logger.critical("example CRITICAL message")

            return True

        except ImportError as e:
            print(_(f"Module import exception: {e}"))
        except KeyError as e:
            print(_(f"Logging configuration error: missing key {e}"))
        except Exception as e:
            print(_(f"An error occurred while setting up logging: {e}"))

    def get(self, request: Request) -> Response:
        """
        Performs all checks and returns their results as a JSON response.

        :param request: The rest_framework Request object.

        :return: Response with the results of all checks.
        """

        # Finds all methods that are checks (decorated with check_method)
        checks = [
            method
            for name, method in inspect.getmembers(self, predicate=inspect.ismethod)
            if getattr(method, "__is_check_method__", False)
        ]
        for check in checks:
            check()

        return Response(self.data)
