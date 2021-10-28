from random import randint, choices
from datetime import timedelta
import string

from django.utils.timezone import now

from . import models as shorten_link_model


def expire_at():
    now_time = now()
    time_delta = timedelta(days=7)
    expire_date = now_time + time_delta
    return expire_date


def generate_token():
    random_int = randint(8, 18)
    generated_random_token = ''.join(choices(
        string.ascii_lowercase + string.digits,
        k=random_int))

    short_link_manager = shorten_link_model.ShortLink.objects

    if short_link_manager.filter(token=generated_random_token).exists():
        return generate_token()

    return generated_random_token
