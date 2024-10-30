from django.db import models
from django.utils.translation import gettext_lazy as _

from hackathons.models.hackathons import Hackathon
from profiles.models.profiles import Profile


class ParticipantsInHackathon(models.Model):
    participant = models.AutoField(primary_key=True, verbose_name=_("participant"))
    hackathon = models.ForeignKey(to=Hackathon, null=True, on_delete=models.SET_NULL, verbose_name=_("hackathon"))
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name=_("profile"))

    def __str__(self):
        return f"{self.participant} | {self.hackathon} | {self.profile}"
