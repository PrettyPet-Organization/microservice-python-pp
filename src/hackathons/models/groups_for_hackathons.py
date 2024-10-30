from django.db import models
from django.utils.translation import gettext_lazy as _

from hackathons.models.groups_in_hackathon import GroupsInHackathon


class GroupsForHackathon(models.Model):
    group = models.ForeignKey(to=GroupsInHackathon, on_delete=models.CASCADE, verbose_name=_("group"))
    group_name = models.CharField(blank=True, null=True, max_length=40, verbose_name=_("group name"))

    def __str__(self):
        return f"{self.group} | {self.group_name}"
