from django.contrib import admin

from projects.models.projects import Project
from projects.models.project_types import ProjectType
from projects.models.roles_in_project import RolesInProject
from projects.models.tools_in_project import ToolsInProject


class ProjectNameMixin:
    """Mixin to display project names in admin models."""

    def project_name(self, obj):
        """Display tools name"""
        return obj.project.project_name

    project_name.short_description = "Project"


class FinishedStatusFilter(admin.SimpleListFilter):
    """Custom filter for Project model to filter it by finished status"""

    title = "Finished"
    parameter_name = "finished_status"

    def lookups(self, request, model_admin):
        return (
            ("finished", ("Finished")),
            ("not_finished", ("Not Finished")),
        )

    def queryset(self, request, queryset):
        if self.value() == "finished":
            return queryset.filter(status=Project.ProjectStatus.FINISHED)
        if self.value() == "not_finished":
            return queryset.exclude(status=Project.ProjectStatus.FINISHED)
        return queryset


@admin.register(Project)
class AdminProject(admin.ModelAdmin):
    """
    Admin interface for the Project model.

    Customizes the display and management of the AdminProject model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        readonly_fields (tuple): Non-editable fields in the admin panel.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
        fieldsets (tuple): Defines the layout of the admin form with grouped fields.
    """

    list_display = (
        "project_name",
        "core_idea",
        "status",
        "finish_date",
        "is_finished",
        "tool_name",
        "role_name",
        "tag_name",
    )
    readonly_fields = ("is_finished",)
    search_fields = ("project_name", "core_idea", "description")
    list_filter = (FinishedStatusFilter, "status", "project_type", "tags", "groups")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "project_name",
                    "core_idea",
                    "description",
                    "finish_date",
                    "status",
                )
            },
        ),
        (("Relations"), {"fields": ("project_type", "tags", "groups")}),
    )

    def tool_name(self, obj):
        """Display the name of the associated hackathon."""
        tools = ", ".join([tool.tool_name for tool in obj.tools.all()])
        return tools

    tool_name.short_description = "Tool"

    def role_name(self, obj):
        """Display the name of the associated hackathon."""
        roles = ", ".join([role.role_name for role in obj.roles.all()])
        return roles

    role_name.short_description = "Role"

    def tag_name(self, obj):
        """Display the name of the associated hackathon."""
        tags = ", ".join([tag.tag_name for tag in obj.tags.all()])
        return tags

    tag_name.short_description = "Tag"


@admin.register(ProjectType)
class AdminProjectTypes(admin.ModelAdmin):
    """
    Admin interface for the ProjectType model.

    Customizes the display and management of the AdminProjectTypes model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
    """

    list_display = ("type_name",)
    search_fields = ("type_name",)


@admin.register(RolesInProject)
class AdminRolesInProject(admin.ModelAdmin, ProjectNameMixin):
    """
    Admin interface for the RolesInProject model.

    Customizes the display and management of the AdminRolesInProject model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = (
        "role_name",
        "project_name",
        "participants_needed",
    )
    search_fields = ("role", "project")
    list_filter = ("role", "project", "participants_needed")

    def role_name(self, obj):
        """Display tools name"""
        return obj.role.role_name

    role_name.short_description = "Role"


@admin.register(ToolsInProject)
class AdminToolsInProject(admin.ModelAdmin, ProjectNameMixin):
    """
    Admin interface for the ToolsInProject model.

    Customizes the display and management of the AdminToolsInProject model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = (
        "tool_name",
        "project_name",
        "participants_needed",
    )
    search_fields = ("tool", "project")
    list_filter = ("tool", "project", "participants_needed")

    def tool_name(self, obj):
        """Display tools name"""
        return obj.tool.tool_name

    tool_name.short_description = "Tool"