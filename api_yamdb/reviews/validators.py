from django.utils import timezone
from django.core.exceptions import ValidationError


def year_validator(value):
    if 1900 > value > timezone.now().year:
        raise ValidationError(
            ('%(value)s некорректный год!'), params={'value': value},)
