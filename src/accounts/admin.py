from django.contrib import admin

from accounts.models.custom_user import CustomUser


@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    """
    Admin interface for the CustomUser model.

    Customizes the display and management of the AdminCustomUser model.

    Attributes:
        list_display (tuple): Fields displayed in the user list view.
        list_editable (tuple): Fields editable in the list view.
        readonly_fields (tuple): Non-editable fields in the admin panel.
        search_fields (tuple): Searchable fields in the admin panel.
        list_filter (tuple): Fields for filtering users in the admin panel.
        fieldsets (tuple): Defines the layout of the admin form with grouped fields
    """

    list_display = (
        "username",
        "email",
        "phone_number",
        "date_joined",
        "is_superuser",
        "is_active",
        "is_staff",
    )
    list_editable = ("is_superuser", "is_active", "is_staff")
    readonly_fields = ("date_joined", "last_login")
    search_fields = ("username", "email", "phone_number")
    list_filter = ("is_active", "is_staff", "is_superuser")
    fieldsets = (
        (
            "Permissions & Status",
            {
                "fields": (
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_staff",
                    "is_active",
                )
            },
        ),
        (
            "User Info",
            {"fields": ("username", "email", "phone_number")},
        ),
        (
            "Important Dates",
            {
                "fields": ("date_joined", "last_login"),
                "classes": ("collapse",),
            },
        ),
    )
