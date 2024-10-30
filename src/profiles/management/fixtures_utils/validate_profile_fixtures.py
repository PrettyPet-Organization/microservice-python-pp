from django.core.exceptions import ValidationError

from profiles.models import Profile


def validate_profile_fixtures() -> None:
    profiles = Profile.objects.all()
    for profile in profiles:
        try:
            profile.clean()

        except Exception as e:
            raise ValidationError(f"Profile: {profile.pk}: {e}")
