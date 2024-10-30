from django.db import models
from django.utils.translation import gettext_lazy as _


class Hobby(models.Model):
    """
    Hobby model.

    Represents a hobby that a user (Profile) can have. Each hobby has a unique name.
    """

    hobby_name = models.CharField(unique=True, max_length=255, verbose_name=_("Hobby name"))

    def __str__(self) -> str:
        return self.hobby_name
