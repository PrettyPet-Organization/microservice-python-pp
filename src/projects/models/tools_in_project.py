from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.tools import Tool
from .participants_in_project import ParticipantInProject


class ToolsInProject(models.Model):
    participant = models.ForeignKey(
        to="ParticipantInProject", on_delete=models.CASCADE, verbose_name=_("Participant")
    )
    tool = models.ForeignKey(
        to=Tool, on_delete=models.SET_NULL, null=True, verbose_name=_("Tool")
    )
    project = models.ForeignKey(
        to="Project", on_delete=models.CASCADE, verbose_name=_("Project")
    )
    participants_needed = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Participants needed")
    )
    
