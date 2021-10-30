from django.urls.exceptions import NoReverseMatch
from django.urls import reverse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


def concatenate_base_url_with_end_point_path(request, end_point_pattern):
    # either end_point_pattern can be a path pattern of view like "user:login" that \
    # refers to login end point of url or can be an token end point for accessing original url

    try:
        # error occurs when we have token instead of patten of path like "user:login"
        path = reverse(end_point_pattern)
    except NoReverseMatch:
        path = "/" + end_point_pattern

    base_url = request.build_absolute_uri('/')[:-1]
    full_url = "{}{}".format(base_url, path)
    
    return full_url


def get_cache_ttl():
    """get cache time to live from django settings"""

    CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
    return CACHE_TTL
