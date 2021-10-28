from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_expire_time(expiration_time):
    now_time = now()

    if expiration_time < now_time:
        raise ValidationError("Expiration time must be bigger than now")


def check_token_min_length(shorten_link):
    if len(shorten_link) < 8:
        raise ValidationError(
            "this field must be at least 8 character")

