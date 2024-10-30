from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    """
    City model.

    Represents a city where users of the platform are from.
    """

    city_name = models.CharField(unique=True, max_length=255, verbose_name=_("City Name"))

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
