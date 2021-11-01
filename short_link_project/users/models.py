from re import T
from django.db import models
from django.contrib.auth import get_user_model


class UserOTPCode(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE
    )

    secret_key = models.CharField(max_length=250, unique=True)

    otp_code = models.IntegerField(unique=True)

    def __str__(self) -> str:
        return f'{self.otp_code}'
    
    def update_then_return_obj(self, secret_key_value, otp_code_value):
        self.otp_code = otp_code_value
        self.secret_key = secret_key_value
        self.save()
        return self
        