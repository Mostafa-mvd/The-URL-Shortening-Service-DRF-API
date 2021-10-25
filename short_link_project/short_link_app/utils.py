from django.utils.timezone import now
from django.core.exceptions import ValidationError

from datetime import timedelta
from datetime import datetime

from random import randint, choices
import string

from . import models as shorten_link_model


def expire_at():
    now_time = now()
    time_delta = timedelta(days=7)
    expire_date = now_time + time_delta
    return expire_date


def validate_expire_time(expiration_time):
    now_time = now()

    if expiration_time < now_time:
        raise ValidationError("Expiration time must be bigger than now")


def create_shorten_link():
    random_int = randint(8, 18)
    random_shorten_link = ''.join(choices(
        string.ascii_lowercase + string.digits, 
        k=random_int))
    
    shorten_link_objects = shorten_link_model.ShortLinkCreator.objects
    
    if shorten_link_objects.filter(shorten_link=random_shorten_link).exists():
        return create_shorten_link()
    
    return random_shorten_link


def format_string_to_readable_datetime(datetime_str):
    datetime_obj = datetime.fromisoformat(datetime_str)
    formated_datetime = datetime_obj.strftime("%Y-%m-%d , %H:%M:%S")
    return formated_datetime


def add_to_redirect_items_field(shorten_link_obj):
    shorten_link_obj.redirected_times += 1
    shorten_link_obj.save()
