from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.roles import Role
from hackathons.models.participants_in_hackathon import ParticipantsInHackathon


class ParticipantInHackathonRoles(models.Model):
    participant = models.ForeignKey(
        to=ParticipantsInHackathon,
        verbose_name=_("participant"),
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(to=Role, null=True, on_delete=models.SET_NULL, verbose_name=_("role"))

    def __str__(self):
        return f"{self.participant} | {self.role}"
