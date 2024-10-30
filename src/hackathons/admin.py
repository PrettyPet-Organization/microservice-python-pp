from django.contrib import admin

from hackathons.models.hackathons import Hackathon
from hackathons.models.groups_in_hackathon import GroupsInHackathon
from hackathons.models.groups_for_hackathons import GroupsForHackathon
from hackathons.models.participants_in_hackathon import ParticipantsInHackathon
from hackathons.models.hackathon_prizes import HackathonPrizes
from hackathons.models.roles_in_hackathon import RolesInHackathon
from hackathons.models.tags_in_hackathon import TagsInHackathon
from hackathons.models.tools_in_hackathon import ToolsInHackathon


class HackathonNameMixin:
    """Mixin to display hackathon names in admin models."""

    def hackathon_name(self, obj):
        """Display the name of the associated hackathon."""
        return obj.hackathon.name

    hackathon_name.short_description = "Hackathon"


@admin.register(Hackathon)
class AdminHackaton(admin.ModelAdmin):
    """
    Admin interface for the Hackaton model.

    Customizes the display and management of the AdminHackaton model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        readonly_fields (tuple): Non-editable fields in the admin panel.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
        fieldsets (tuple): Defines the layout of the admin form with grouped fields.
    """

    list_display = (
        "hackathon",
        "type",
        "name",
        "core_idea",
        "task",
        "start_date",
        "finish_date",
        "image_url",
        "prize_name",
    )
    readonly_fields = (
        "hackathon",
        "start_date",
    )
    search_fields = (
        "name",
        "core_idea",
        "task",
    )
    list_filter = (
        "type",
        "start_date",
        "finish_date",
    )
    fieldsets = (
        (
            "General Info",
            {
                "fields": (
                    "name",
                    "type",
                    "core_idea",
                    "task",
                )
            },
        ),
        (
            "Date Info",
            {
                "fields": ("start_date", "finish_date"),
            },
        ),
        (
            "Media",
            {
                "fields": ("image_url",),
            },
        ),
        (
            "Prizes & Relations",
            {
                "fields": ("prize_id",),
            },
        ),
    )

    def prize_name(self, obj):
        """Display HackathonPrizes for the Hackathon."""
        prizes = obj.hackathonprizes_set.all()
        return ", ".join([f"{prize.name}" for prize in prizes])

    prize_name.short_description = "Prize"


@admin.register(GroupsInHackathon)
class AdminGroupsInHackathon(admin.ModelAdmin):
    """
    Admin interface for the GroupsInHackathon model.

    Customizes the display and management of the AdminGroupsInHackathon model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = ("group", "hackathon")
    search_fields = ("group", "hackathon")
    list_filter = ("hackathon",)


@admin.register(GroupsForHackathon)
class AdminGroupsForHackathon(admin.ModelAdmin):
    """
    Admin interface for the GroupsForHackaton model.

    Customizes the display and management of the AdminGroupsForHackathon model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = ("group", "group_name")
    search_fields = ("group", "group_name")
    list_filter = ("group",)


@admin.register(ParticipantsInHackathon)
class AdminParticipantsInHackathon(admin.ModelAdmin, HackathonNameMixin):
    """
    Admin interface for the ParticipantsInHackathon model.

    Customizes the display and management of the AdminParticipantsInHackathon model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = (
        "participant",
        "hackathon_name",
        "profile",
    )
    search_fields = ("hackathon_name", "profile")
    list_filter = ("hackathon", "profile")


@admin.register(HackathonPrizes)
class AdminHackathonPrizes(admin.ModelAdmin):
    """
    Admin interface for the HackathonPrizes model.

    Customizes the display and management of the AdminHackathonPrizes model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
    """

    list_display = (
        "hackathon_name",
        "name",
        "description",
        "image_url",
    )
    search_fields = ("name",)

    def hackathon_name(self, obj):
        """Display the name of the associated hackathon."""
        hackathon = ", ".join([hackathon.name for hackathon in obj.prize.all()])
        return hackathon

    hackathon_name.short_description = "Hackathon"


@admin.register(RolesInHackathon)
class AdminRolesInHackathon(admin.ModelAdmin, HackathonNameMixin):
    """
    Admin interface for the RolesInHackathon model.

    Customizes the display and management of the AdminRolesInHackathon model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = ("hackathon_name", "role_name", "participants_needed")
    list_filter = ("role", "participants_needed")

    def role_name(self, obj):
        """Display tools name"""
        return obj.role.role_name

    role_name.short_description = "Role"


@admin.register(TagsInHackathon)
class AdminTagsInHackathon(admin.ModelAdmin, HackathonNameMixin):
    """
    Admin interface for the TagsInHackathon model.

    Customizes the display and management of the AdminTagsInHackathon model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = ("hackathon_name", "tag_name")
    search_fields = ("tag",)
    list_filter = ("tag",)

    def tag_name(self, obj):
        """Display tools name"""
        return obj.tag.tag_name

    tag_name.short_description = "Tag"


@admin.register(ToolsInHackathon)
class AdminToolsInHackathon(admin.ModelAdmin, HackathonNameMixin):
    """
    Admin interface for the ToolsInHackathon model.

    Customizes the display and management of the AdminToolsInHackathon model.


    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = ("hackathon_name", "tool_name", "participants_needed")
    search_fields = ("tool", "participants_needed")
    list_filter = ("tool", "participants_needed")

    def tool_name(self, obj):
        """Display tools name"""
        return obj.tool.tool_name

    tool_name.short_description = "Tool"