from django.core import validators
from django.db import models
from . import utils as shortener_links_utils


class ShortLinkCreator(models.Model):

    original_url = models.URLField(
        validators=[
            validators.URLValidator([
                'http', 
                'https',
            ]),
        ]
    )

    shorten_url = models.CharField(
        unique=True,
        max_length=18,
        blank=True
    )

    created_time = models.DateTimeField(
        auto_now_add=True
    )
    
    expiration_time = models.DateTimeField(
        default=shortener_links_utils.expire_at,
        validators=[
            shortener_links_utils.validate_expire_time,
        ]
    )

    redirected_times = models.PositiveIntegerField(
        default=0
    )

    is_shorten_url_private = models.BooleanField(
        default=False,
        verbose_name="Private URL?"
    )

    def __str__(self):
        return "{} -> {}".format(self.original_url, self.shorten_url)
