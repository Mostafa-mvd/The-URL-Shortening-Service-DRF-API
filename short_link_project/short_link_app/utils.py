from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError


def expire_at():
    now_time = now()
    time_delta = timedelta(days=7)
    expire_date = now_time + time_delta
    return expire_date


def validate_expire_time(expiration_time):
    now_time = now()

    if expiration_time < now_time:
        raise ValidationError("Expiration time must be bigger than now")
