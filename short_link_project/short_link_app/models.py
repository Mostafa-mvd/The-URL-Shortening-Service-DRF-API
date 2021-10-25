from django.core import validators
from django.db import models
from . import utils as shortener_links_utils
from django.db.models.functions import Length


models.CharField.register_lookup(Length)


class ShortLinkCreator(models.Model):

    original_url = models.URLField(
        validators=[
            validators.URLValidator([
                'http', 
                'https',
            ]),
        ]
    )

    shorten_link = models.CharField(
        default=shortener_links_utils.create_shorten_link,
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

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(shorten_link__length__gte=8),
                name="Check constraints for shorten_link field that must be gte 8",
            )
        ]

        ordering = [
            "-created_time"
        ]

    def __str__(self):
        return "{} -> {}".format(self.original_url, self.shorten_link)
