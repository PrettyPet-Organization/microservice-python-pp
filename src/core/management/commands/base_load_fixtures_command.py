from typing import (
    Any,
    Callable,
)

from django.core.management import BaseCommand


class BaseLoadFixturesCommand(BaseCommand):
    handle_func: Callable[[], None]
    success_message: str
    error_message: str

    @classmethod
    def _handle_func(cls) -> None:
        """
        This wrapper is necessary to prevent passing `self` to the `handle_func` as an argument.
        """

        return cls.handle_func()

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            self._handle_func()
            self.stdout.write(self.style.SUCCESS(self.success_message))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"{self.error_message}: {str(e)}"))
