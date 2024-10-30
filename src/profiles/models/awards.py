from django.db import models
from django.utils.translation import gettext_lazy as _


class Award(models.Model):
    """
    Award model.

    Awards are given by the platform to users (Profile) for achievements or participation in various events.
    Each award has a unique name.
    """

    award_name = models.CharField(max_length=255, unique=True, verbose_name=_("Award Name"))
    description = models.TextField(verbose_name=_("Award Description"))
    image_url = models.URLField(verbose_name=_("Award Image URL"))

    def __str__(self):
        return self.award_name

    class Meta:
        verbose_name = _("Award")
        verbose_name_plural = _("Awards")
