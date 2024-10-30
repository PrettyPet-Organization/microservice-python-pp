from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.roles import Role
from common.models.tags import Tag
from common.models.tools import Tool


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        NOT_STARTED = "NS", _("Not Started")
        IN_PROCESS = "IP", _("In Process")
        NOT_FINISHED = "NF", _("Not Finished")
        FINISHED = "FN", _("Finished")

    project_type = models.ForeignKey(
        to="ProjectType",
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects",
        verbose_name=_("Type for project"),
    )
    project_name = models.CharField(verbose_name=_("Project name"), max_length=100)
    core_idea = models.CharField(verbose_name=_("Core idea"), max_length=255)
    description = models.TextField(verbose_name=_("Description"))
    finish_date = models.DateField(verbose_name=_("End time for project"), null=True, blank=True)
    status = models.CharField(
        verbose_name=_("Actual status"),
        max_length=2,
        choices=ProjectStatus.choices,
        default=ProjectStatus.NOT_STARTED,
    )
    tools = models.ManyToManyField(
        to=Tool,
        through="ToolsInProject",
        related_name="projects",
        verbose_name=_("Tools for project"),
    )
    roles = models.ManyToManyField(
        to=Role,
        through="RolesInProject",
        related_name="projects",
        verbose_name=_("Role for project"),
    )
    tags = models.ManyToManyField(to=Tag, related_name="projects", verbose_name=_("Tags for project"))
    groups = models.ManyToManyField(to="Group", related_name="projects", verbose_name=_("Groups for project"))

    @property
    def is_finished(self):
        return self.status == self.ProjectStatus.FINISHED

    def __str__(self):
        return f"Project №{self.pk} - {self.project_name}"
