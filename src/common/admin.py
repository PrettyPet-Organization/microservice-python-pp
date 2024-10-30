from django.contrib import admin

from common.models.news import News
from common.models.roles import Role
from common.models.tags import Tag
from common.models.tools import Tool
from common.models.topics import Topic
from common.models.useful_materials import UsefulMaterial


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    """
    Admin interface for the News model.

    Customizes the display and management of the AdminNews model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        list_editable (tuple): Fields editable in the list view.
        readonly_fields (tuple): Non-editable fields in the admin panel.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
        fieldsets (tuple): Defines the layout of the admin form with grouped fields.
    """

    list_display = (
        "title",
        "author_info",
        "is_open",
        "likes",
        "topics_list",
        "tags_list",
        "image_url",
    )

    list_editable = ("is_open",)
    search_fields = ("title", "description", "author")
    list_filter = ("is_open", "topics", "author", "tags")
    readonly_fields = ("likes",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "image_url",
                    "author",
                    "likes",
                    "is_open",
                )
            },
        ),
        (
            ("Relations"),
            {
                "fields": ("topics", "tags"),
            },
        ),
    )

    def topics_list(self, obj):
        "Display topics related to news"
        if obj.topics:
            return ", ".join([topic.topic_name for topic in obj.topics.all()])
        else:
            return "No Topics"

    topics_list.short_description = "Topics"

    def tags_list(self, obj):
        """Display tags related to the news."""
        return obj.tags.tag_name if obj.tags else "No Tags"

    tags_list.short_description = "Tags"

    def author_info(self, obj):
        """Display author's profile_id and public_name from Profile Model"""
        return f"ID: {obj.author.id}, Name: {obj.author.public_name}"

    author_info.short_description = "Author"


@admin.register(Role)
class AdminRoles(admin.ModelAdmin):
    """
    Admin interface for the Role model.

    Customizes the display and management of the AdminRoles model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
    """

    list_display = ("role_name",)
    search_fields = ("role_name",)


@admin.register(Tag)
class AdminTags(admin.ModelAdmin):
    """
    Admin interface for the Tag model.

    Customizes the display and management of the AdminTags model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
    """

    list_display = ("tag_name",)
    search_fields = ("tag_name",)


@admin.register(Tool)
class AdminTools(admin.ModelAdmin):
    """
    Admin interface for the Tool model.

    Customizes the display and management of the AdminTools model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
    """

    list_display = ("tool_name",)
    search_fields = ("tool_name",)


@admin.register(Topic)
class AdminTopic(admin.ModelAdmin):
    """
    Admin interface for the Topic model.

    Customizes the display and management of the AdminTopic model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
    """

    list_display = ("topic_name",)
    search_fields = ("topic_name",)


@admin.register(UsefulMaterial)
class AdminUsefulMaterials(admin.ModelAdmin):
    """
    Admin interface for the UsefulMaterial model.

    Customizes the display and management of the AdminUsefulMaterials model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = (
        "title",
        "description",
        "image_url",
        "likes",
        "link_name",
    )
    search_fields = ("title", "link_name")
    list_filter = ("likes",)