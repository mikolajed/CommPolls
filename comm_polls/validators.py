from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class NumberValidator:
    """
    Validates that the password contains at least one digit.
    """
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("This password must contain at least one digit."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _("Your password must contain at least one digit.")

class UppercaseValidator:
    """
    Validates that the password contains at least one uppercase letter.
    """
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter.")