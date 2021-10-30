from django.contrib.auth import get_user_model
from django.conf import settings
from users import models as users_models
import pyotp


def get_otp_code_ttl():
    """get otp code time to live from django settings,
        result is in seconds"""

    OTP_DEFAULT_TIMEOUT = 60 * 5
    OPT_CODE_TTL = getattr(settings, 'OTP_TTL', OTP_DEFAULT_TIMEOUT)
    return OPT_CODE_TTL

def generate_user_secret_key(user_id):

    user_obj = get_user_model().objects.get(id=user_id)

    secret_key_str = pyotp.random_base32()

    if users_models.UserSecretKey.objects.filter(user_secret_key=secret_key_str).exists():
        return generate_user_secret_key(user_id)

    secret_key_obj = users_models.UserSecretKey.objects.create(
        user=user_obj,
        user_secret_key=secret_key_str)

    secret_key_obj.save()

def generate_totp_code(user_obj):
    secret_key_obj = users_models.UserSecretKey.objects.get(
        user=user_obj)

    totp = pyotp.TOTP(
        s=secret_key_obj.user_secret_key, 
        interval=get_otp_code_ttl())
        
    otp_code = totp.now()

    return otp_code

def is_totp_code_valid(totp_code, user_obj):
    secret_key_obj = users_models.UserSecretKey.objects.get(user=user_obj)

    totp = pyotp.TOTP(
        s=secret_key_obj.user_secret_key, 
        interval=get_otp_code_ttl())

    is_valid = totp.verify(totp_code)

    if not is_valid:
        return False
    return True
