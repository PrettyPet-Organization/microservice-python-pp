from django.contrib import admin

from profiles.models.profiles import Profile
from profiles.models.cities import City


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    """
    Admin interface for the Profile model.

    Customizes the display and management of the AdminProfile model.


    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        readonly_fields (tuple): Non-editable fields in the admin panel.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
    """

    list_display = (
        "user",
        "public_name",
        "city__city_name",
        "photo_url",
    )
    search_fields = (
        "user__username",
        "public_name",
        "city__city_name",
    )
    list_filter = ("city",)

    readonly_fields = ("photo_url",)


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    """
    Admin interface for the City model.

    Customizes the display and management of the AdminCity model.


    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        search_fields (tuple): Searchable fields in the admin panel.
    """

    list_display = ("city_name",)
    search_fields = ("city_name",)
