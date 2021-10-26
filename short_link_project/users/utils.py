

from users import models
from django.contrib.auth import get_user_model
from users import models as users_models
import pyotp


def generate_user_secret_key(user_id):

    user_obj = get_user_model().objects.get(id=user_id)

    secret_key_str = pyotp.random_base32()
    secret_key_obj = models.UserSecretKey.objects.create(
        user=user_obj,
        user_secret_key=secret_key_str)

    secret_key_obj.save()


def generate_otp_code(user_obj):
    secret_key_obj = users_models.UserSecretKey.objects.get(
        user=user_obj)

    totp = pyotp.TOTP(secret_key_obj.user_secret_key, interval=120)
    otp_code = totp.now()

    return otp_code


def is_otp_code_valid(otp_code, user_obj):
    secret_key_obj = users_models.UserSecretKey.objects.get(user=user_obj)
    totp = pyotp.TOTP(secret_key_obj.user_secret_key, interval=120)
    is_valid = totp.verify(otp_code)

    if not is_valid:
        return False
    return True
