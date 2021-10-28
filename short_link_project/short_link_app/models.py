from django.core import validators as django_validators
from django.db import models

from . import validators as shortener_links_validators
from . import defaults as shortener_defaults_fields


class ShortLink(models.Model):

    original_url = models.URLField(
        validators=[
            django_validators.URLValidator([
                'http', 
                'https',
            ]),
        ],
        max_length=1024
    )

    token = models.CharField(
        default=shortener_defaults_fields.generate_token,
        unique=True,
        max_length=18,
        validators=[
            django_validators.RegexValidator(r'[\w-]{8,18}'),
            shortener_links_validators.check_token_min_length
        ]
    )

    created_time = models.DateTimeField(
        auto_now_add=True
    )
    
    expiration_time = models.DateTimeField(
        default=shortener_defaults_fields.expire_at,
        validators=[
            shortener_links_validators.validate_expire_time,
        ]
    )

    times_of_redirected = models.PositiveIntegerField(
        default=0
    )

    is_private = models.BooleanField(
        default=False,
        verbose_name="Private URL?"
    )

    class Meta:
        verbose_name = 'ShortLink'
        verbose_name_plural = 'ShortLinks'
        ordering = [
            "-created_time"
        ]

    def __str__(self):
        return "{} -> {}".format(self.original_url, self.token)
    
    def get_formated_created_time_str(self):
        return self.created_time.strftime('%Y-%m-%d, %H:%M:%S')
    
    def get_formated_expiration_time_str(self):
        return self.expiration_time.strftime('%Y-%m-%d, %H:%M:%S')
    
    def add_to_times_of_redirected_field(self):
        self.times_of_redirected += 1
        self.save()
