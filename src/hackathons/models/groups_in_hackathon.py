from django.db import models
from django.utils.translation import gettext_lazy as _

from hackathons.models.hackathons import Hackathon


class GroupsInHackathon(models.Model):
    group = models.IntegerField(unique=True, verbose_name=_("group"))
    hackathon = models.ForeignKey(to=Hackathon, null=True, on_delete=models.SET_NULL, verbose_name=_("hackathon"))

    def __str__(self):
        return f"{self.group} | {self.hackathon}"
