from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.tools import Tool
from hackathons.models.participants_in_hackathon import ParticipantsInHackathon


class ParticipantInHackathonTools(models.Model):
    participant = models.ForeignKey(
        to=ParticipantsInHackathon,
        on_delete=models.CASCADE,
        verbose_name=_("participant id"),
    )
    tool = models.ForeignKey(to=Tool, null=True, on_delete=models.SET_NULL, verbose_name=_("tool"))

    def __str__(self):
        return f"{self.participant} | {self.tool}"
