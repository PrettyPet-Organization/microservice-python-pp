from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.tags import Tag
from hackathons.models.hackathons import Hackathon


class TagsInHackathon(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, null=True, on_delete=models.SET_NULL, verbose_name=_("hackathon"))
    tag = models.ForeignKey(to=Tag, null=True, on_delete=models.SET_NULL, verbose_name=_("tag"))

    def __str__(self):
        return f"{self.hackathon} | {self.tag}"
