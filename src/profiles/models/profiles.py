from datetime import (
    date,
    datetime,
)
from typing import (
    Iterable,
    Optional,
    Union,
)

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateField,
    ForeignKey,
    ManyToManyField,
    Model,
    OneToOneField,
    TextField,
    URLField,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from accounts.models import CustomUser
from profiles.models import (
    awards,
    cities,
    hobbies,
    profile_roles,
)
from profiles.validators import MaxAgeValidator


class Profile(Model):
    """
    User profile model.

    Represents user public information and skills.
    """

    MAX_AGE = 150
    MAX_NUMBER_OF_HOBBIES = 15
    MAX_NUMBER_OF_ROLES = 3

    _birth_date = DateField(blank=True, null=True, verbose_name=_("Birth Date"), validators=[MaxAgeValidator(MAX_AGE)])
    description = TextField(blank=True, null=True, verbose_name=_("Description"))
    photo_url = URLField(blank=True, null=True, verbose_name=_("Photo URL"))
    public_name = CharField(max_length=255, blank=True, null=True, verbose_name=_("Public Name"))

    user = OneToOneField(CustomUser, on_delete=CASCADE, related_name="profile", verbose_name=_("User"))

    city = ForeignKey(cities.City, on_delete=SET_NULL, blank=True, null=True, verbose_name=_("City"))

    awards = ManyToManyField(awards.Award, blank=True, verbose_name=_("Awards"))
    favourite_materials = ManyToManyField("common.UsefulMaterial", blank=True, verbose_name=_("Favourite Materials"))
    hobbies = ManyToManyField(hobbies.Hobby, blank=True, verbose_name=_("Hobbies"))
    roles = ManyToManyField("common.Role", blank=True, through=profile_roles.ProfileRole, verbose_name=_("Roles"))
    social_links = ManyToManyField("common.SocialLink", blank=True, verbose_name=_("Social Links"))
    subscriptions = ManyToManyField("self", blank=True, symmetrical=False, verbose_name=_("Subscriptions"))
    tools = ManyToManyField("common.Tool", blank=True, verbose_name=_("Tools"))

    def __str__(self) -> str:
        return self.public_name

    def _validate_number_of_hobbies(self) -> None:
        """
        Validates the number of hobbies associated with a user profile.

        Checks if the count of hobbies exceeds the maximum allowed limit (`MAX_NUMBER_OF_HOBBIES`).

        :raises ValidationError: if the number of hobbies exceeds the maximum allowed limit.
        """

        if self.hobbies.count() > self.MAX_NUMBER_OF_HOBBIES:
            raise ValidationError(_(f"Number of hobbies must be less than or equal to {self.MAX_NUMBER_OF_HOBBIES}"))

    def _validate_roles(self) -> None:
        """
        Validates the roles associated with a user profile.

        Checks that the number of roles does not exceed the maximum allowed limit
        and that the user has exactly one primary role.

        :raises ValidationError: if the number of roles exceeds the maximum allowed limit
        or if the user does not have exactly one primary role.
        """

        if self.roles.count() > self.MAX_NUMBER_OF_ROLES:
            raise ValidationError(_(f"Number of roles must be less than or equal to {self.MAX_NUMBER_OF_ROLES}"))

        # If the user (Profile) has roles and there are more than 1 of them
        if self.profilerole_set.filter(is_main=True).count() not in (0, 1):
            raise ValidationError(_("User must have exactly one main role"))

    def _validate_subscriptions(self) -> None:
        """
        Validates the subscriptions associated with a user (Profile).

        Checks that the user (Profile) cannot subscribe to themselves.

        :raises ValidationError: if the user tries to subscribe to themselves.
        """

        if self.subscriptions.filter(pk=self.pk).exists():
            raise ValidationError(_("User cannot subscribe to themselves."))

    # TODO: Replace this property with a scheduled task to update `age` field periodically to avoid extra calculations.
    @property
    def age(self) -> Optional[int]:
        """
        Calculates the user's age based on their birth date.

        :return: The user's age in years, or `None` if the birth date is not set.
        """

        if self.birth_date:
            return relativedelta(date.today(), self.birth_date).years
        return None

    @property
    def birth_date(self) -> Optional[date]:
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: Optional[Union[date, str]]) -> None:
        """
        Custom setter to ensure that the `_birth_date` field is always a datetime.date object.

        The reason to use the setter is to validate the value on the Python level and to ensure that the `_birth_date`
        field is always a datetime.date object. The default behavior of the DateField is to accept any value
        and validate values only when saving an object to the db, but this can lead to unexpected behavior
        and errors when working with the object on the Python level. By using the setter, we can ensure that the value
        is always a datetime.date object.

        :param value: The new value for the `_birth_date` field.

        :raises TypeError: if the `value` is not a string or a datetime.date object.
        """

        if isinstance(value, Optional[Union[date, str]]):
            if isinstance(value, str):
                value = datetime.strptime(value, "%Y-%m-%d").date()
            self._birth_date = value
        else:
            raise TypeError(_("Birth date should be a string in the format 'YYYY-MM-DD' or a datetime.date object"))

    def clean(self) -> None:
        self._validate_number_of_hobbies()
        self._validate_roles()
        self._validate_subscriptions()

        super().clean()

    def save(
        self,
        force_insert: Union[bool, tuple[ModelBase, ...]] = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Union[Iterable[str], None] = None,
    ) -> None:
        self.clean()
        super().save(force_insert, force_update, using, update_fields)

    class Meta(TypedModelMeta):
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
