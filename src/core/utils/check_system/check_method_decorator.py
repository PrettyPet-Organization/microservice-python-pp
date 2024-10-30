from functools import wraps
from typing import (
    Callable,
    Optional,
)

from django.utils.functional import Promise


_CHECK_SYSTEM_VIEW_TYPE = "CheckSystem"
_METHOD_TO_CHECK_TYPE = Callable[[_CHECK_SYSTEM_VIEW_TYPE], Optional[bool]]
_DECORATOR_RETURN_TYPE = Callable[[_CHECK_SYSTEM_VIEW_TYPE], None]
_CHECK_METHOD_TYPE = Callable[[_METHOD_TO_CHECK_TYPE], _DECORATOR_RETURN_TYPE]


def check_method(
    data_item_name: str, error_message: Optional[Promise] = None, success_message: Optional[Promise] = None
) -> _CHECK_METHOD_TYPE:
    """
    Decorator for checking methods.

    Uses the provided check method to perform a check, marks the wrapper method with a custom attribute. If the
    check fails, raises an exception with the specified error message or a default message. Updates the `self.data`
    dictionary with the success message if the check passes.

    :param data_item_name: Name of the data item to store in `self.data`.
    :param error_message: Error message to raise if the check fails. Defaults to None.
    :param success_message: Success message to store in `self.data`. Defaults to None.

    :return: Decorated method that performs the check and updates `self.data`.

    :raises Exception: If the check method fails.
    """

    def decorator(method_to_check: _METHOD_TO_CHECK_TYPE) -> _DECORATOR_RETURN_TYPE:
        @wraps(method_to_check)
        def wrapper(self: _CHECK_SYSTEM_VIEW_TYPE) -> None:
            if not method_to_check(self):
                # If the error message is not specified, uses the default
                raise Exception(
                    error_message if error_message else self.DEFAULT_ERROR_MESSAGE.format(item=method_to_check.__name__)
                )

            # If the success message is not specified, uses the default
            self.data[data_item_name] = success_message if success_message else self.DEFAULT_SUCCESS_MESSAGE

        # Marks the wrapper method with a custom attribute
        wrapper.__is_check_method__ = True  # type: ignore[attr-defined]
        return wrapper

    return decorator
