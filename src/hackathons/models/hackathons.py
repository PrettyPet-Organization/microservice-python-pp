from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Hackathon(models.Model):
    hackathon = models.AutoField(primary_key=True, verbose_name=_("hackathon"))
    type = models.IntegerField(blank=True, null=True, verbose_name=_("type id"))
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name=_("name"))
    core_idea = models.CharField(max_length=40, blank=True, null=True, verbose_name=_("core idea"))
    task = models.TextField(max_length=400, blank=True, null=True, verbose_name=_("task"))
    start_date = models.DateField(default=timezone.now, verbose_name=_("start date"))
    finish_date = models.DateField(blank=True, null=True, verbose_name=_("finish date"))
    image_url = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("image url"))
    prize_id = models.IntegerField(blank=True, null=True, verbose_name=_("prize id"))

    def __str__(self):
        return f"{self.name} | №{self.hackathon}"
