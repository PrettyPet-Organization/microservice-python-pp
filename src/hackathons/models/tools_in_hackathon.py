from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.tools import Tool
from hackathons.models.hackathons import Hackathon


class ToolsInHackathon(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, null=True, on_delete=models.SET_NULL, verbose_name=_("hackathon"))
    tool = models.ForeignKey(to=Tool, null=True, on_delete=models.SET_NULL, verbose_name=_("tool"))
    participants_needed = models.IntegerField(
        default=None, blank=True, null=True, verbose_name=_("participants needed")
    )

    def __str__(self):
        return f"{self.hackathon} | {self.tool}"
