from core.management.commands import BaseLoadFixturesCommand
from profiles.management.fixtures_utils import load_profile_fixtures


class Command(BaseLoadFixturesCommand):
    help = "Populate the database with profile data"
    handle_func = load_profile_fixtures
    success_message = "Profile fixtures successfully loaded!"
    error_message = "WARNING: Profile fixtures loaded, but invalid"
