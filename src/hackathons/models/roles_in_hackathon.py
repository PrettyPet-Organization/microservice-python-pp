from django.db import models
from django.utils.translation import gettext_lazy as _

from hackathons.models.hackathons import Hackathon
from projects.models.roles_in_project import Role


class RolesInHackathon(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, null=True, on_delete=models.SET_NULL, verbose_name=_("hackathon"))
    role = models.ForeignKey(to=Role, null=True, on_delete=models.SET_NULL, verbose_name=_("role"))
    participants_needed = models.IntegerField(
        default=None, blank=True, null=True, verbose_name=_("participants needed")
    )

    def __str__(self):
        return f"{self.hackathon} | {self.role}"
