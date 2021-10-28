from django.urls.exceptions import NoReverseMatch
from django.urls import reverse


def concatenate_domain_with_path(request, end_point_pattern):
    # either end_point_pattern can be a path pattern of view like "user:login" that \
    # refers to login end point of url or can be an token end point for accessing original url

    try:
        # error occurs when we have token instead of patten of path like "user:login"
        path = reverse(end_point_pattern)
    except NoReverseMatch:
        path = "/" + end_point_pattern

    main_domain = request.build_absolute_uri('/')[:-1]
    url = "{}{}".format(main_domain, path)
    
    return url
