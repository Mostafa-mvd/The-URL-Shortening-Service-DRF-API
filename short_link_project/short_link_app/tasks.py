import logging

from celery import shared_task

from django.utils.timezone import now

from . import models as short_link_models

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_short_links():
    short_link_models.ShortLink.objects.filter(expiration_time__lt=now()).delete()
    logger.debug(f"Expired links deleted.")
