import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Checking for a sequence of characters on one keyboard line
def in_keyboard(sub: str) -> bool:
    keyboard_rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

    for row in keyboard_rows:
        if sub in row or sub in row[::-1]:
            return True
    return False


# Password validation
def validate_password(value):
    # Length check
    if len(value) < 8:
        raise ValidationError(_("The password must be at least 8 characters."))

    # Checks for letters and numbers only
    if not re.match("^[A-Za-z0-9]*$", value):
        raise ValidationError(_("The password can only contain letters and numbers."))

    # Checking for at least one capital letter
    if not re.search("[A-Z]", value):
        raise ValidationError(_("The password must contain at least one capital letter."))

    # Substrings of 4 characters
    substrings = [value[i : i + 4] for i in range(len(value) - 3)]

    # Checking whether the correct sequence is found
    if any(in_keyboard(sub.lower()) for sub in substrings):
        raise ValidationError(_("Invalid substring found."))


def validate_phone_number(phone_number: str):
    phone_regex_dict = {
        (
            "+7",
            "+33",
            "+34",
            "+90",
            "+30",
            "+351",
            "+212",
            "+213",
            "+216",
            "+380",
            "+375",
        ): r"\d{3}\d{3}\d{2}\d{2}",
        # xxx xxx xx xx
        (
            "+1",
            "+49",
            "+39",
            "+86",
            "+55",
            "+52",
            "+61",
            "+91",
            "+54",
            "+92",
            "+82",
            "+81",
            "+27",
            "+63",
            "+62",
            "+84",
            "+57",
            "+51",
            "+56",
            "+593",
            "+58",
            "+66",
            "+98",
            "+60",
            "+234",
            "+355",
        ): r"\d{3}\d{3}\d{4}",  # xxx xxx xxxx
        (
            "+44",
            "+353",
            "+31",
            "+46",
            "+47",
            "+358",
            "+45",
            "+41",
            "+43",
            "+64",
        ): r"\d{4}\d{3}\d{3}",  # xxxx xxx xxx
        (
            "+972",
            "+65",
            "+852",
            "+354",
            "+372",
            "+371",
            "+370",
        ): r"\d{2}\d{4}\d{4}",  # xx xxxx xxxx
        ("+32", "+420", "+421", "+48", "+40", "+36"): r"\d{2}\d{3}\d{4}",  # xx xxx xxxx
        ("+385", "+386", "+358"): r"\d\d{3}\d{3}\d{3}",  # x xxx xxx xxx
        ("+45", "+47", "+354"): r"\d{2}\d{2}\d{2}\d{2}",  # xx xx xx xx
        ("+33", "+352", "+370", "+41"): r"\d{3}\d{2}\d{2}\d{2}",  # xxx xx xx xx
    }
    for prefixes, regex in phone_regex_dict.items():
        for prefix in prefixes:
            if phone_number.startswith(prefix):
                # Remove prefix from number for later verification
                local_number = phone_number[len(prefix) :]
                match = re.fullmatch(pattern=regex, string=local_number)
                if not match:
                    raise ValidationError(_(f"Invalid number format for prefix {prefix}."))
                return

    # If no prefix matches
    raise ValidationError(_("Incorrect number prefix."))
