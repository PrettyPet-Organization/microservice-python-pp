from django.core.management import call_command

from profiles.management.fixtures_utils.validate_profile_fixtures import validate_profile_fixtures


def load_profile_fixtures() -> None:
    """
    Loads profile fixtures into the database.
    """

    call_command("loaddata", "accounts/custom_user.json", app_label="core")
    call_command("loaddata", "profiles/awards.json", app_label="core")
    call_command("loaddata", "profiles/cities.json", app_label="core")
    call_command("loaddata", "profiles/hobbies.json", app_label="core")
    call_command("loaddata", "common/roles.json", app_label="core")
    call_command("loaddata", "profiles/profiles.json", app_label="core")
    call_command("loaddata", "profiles/profile_roles.json", app_label="core")

    validate_profile_fixtures()
