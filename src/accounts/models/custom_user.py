from hashlib import sha256

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager
from accounts.validators import validate_password, validate_phone_number


class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(verbose_name=_("Email"), unique=True, max_length=255)
    phone_number = models.CharField(
        verbose_name=_("Phone number"),
        unique=True,
        blank=True,
        null=True,
        default=None,
        max_length=20,
        validators=[validate_phone_number],
    )
    password = models.CharField(
        verbose_name=_("User password"), validators=[validate_password], max_length=255
    )
    first_name = None
    last_name = None
    code_word = models.CharField(
        verbose_name=_("Code word for entry"), max_length=12, blank=True
    )

    objects = CustomUserManager()

    confirmed_form_about_platform = models.BooleanField(
        default=False, blank=True, null=True
    )

    # Set the code word
    def set_code_word(self, code_word):
        self.code_word = sha256(code_word.encode()).hexdigest()

    # Checking for a code word match
    def check_code_word(self, code_word):
        return self.code_word == sha256(code_word.encode()).hexdigest()

    def __str__(self):
        return self.username

    class Meta:
        app_label = "accounts"
