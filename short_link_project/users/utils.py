from django.conf import settings
from users import models as users_models
import pyotp


def get_otp_code_ttl():
    """get otp code time to live from django settings,
        result is in seconds"""

    OTP_DEFAULT_TIMEOUT = 60 * 3
    OPT_CODE_TTL = getattr(settings, 'OTP_TTL', OTP_DEFAULT_TIMEOUT)
    return OPT_CODE_TTL


def is_totp_code_valid(otp_code):
    otp_qs = users_models.UserOTPCode.objects.filter(otp_code=otp_code)

    if otp_qs.exists():
        otp_obj = otp_qs.first()
        totp = pyotp.TOTP(
            s=otp_obj.secret_key,
            interval=get_otp_code_ttl())

        is_valid = totp.verify(otp_code)
        otp_obj.delete()

        if is_valid:
            return True
        return False

    return False
