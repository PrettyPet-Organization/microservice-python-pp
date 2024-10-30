from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Model,
    TextChoices,
)
from django.utils.translation import gettext_lazy as _


class RoleLevel(TextChoices):
    TRAINEE = "trainee", _("Trainee")
    INTERN = "intern", _("Intern")
    JUNIOR = "junior", _("Junior")
    MIDDLE = "middle", _("Middle")
    SENIOR = "senior", _("Senior")


class ProfileRole(Model):
    """
    Intermediate model for linking profiles and roles.

    The user must have a main role.
    """

    is_main = BooleanField(default=False, verbose_name=_("Is Main Role"))
    level = CharField(max_length=7, choices=RoleLevel, verbose_name=_("Level"))
    profile = ForeignKey("Profile", on_delete=CASCADE, verbose_name=_("Profile"))
    role = ForeignKey("common.Role", on_delete=CASCADE, verbose_name=_("Role"))

    def __str__(self):
        return f"profile: {self.profile} | role: {self.role} | {"main" if self.is_main else "secondary"} | level: {self.level}"

    class Meta:
        verbose_name = _("Profile Role")
        verbose_name_plural = _("Profile Roles")
