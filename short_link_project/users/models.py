from django.db import models
from django.contrib.auth import get_user_model


class UserSecretKey(models.Model):

    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE
    )

    user_secret_key = models.TextField()

    def __str__(self) -> str:
        return self.user_secret_key
