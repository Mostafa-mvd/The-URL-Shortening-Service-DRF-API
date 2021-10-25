from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from . import utils
from . import serializers as shorten_link_serializer
from . import models as shorten_Link_model

from django.shortcuts import get_object_or_404, redirect


class CreateShortenLink(generics.CreateAPIView):
    serializer_class = shorten_link_serializer.ShortenLinkSerializer
    model = shorten_Link_model.ShortLinkCreator

    def render_json_result(self, response_data):
        main_domain = self.request.build_absolute_uri('/')
        shorten_link = response_data["result_link"]
        expiration_time = response_data["expiration_time"]

        shorten_url = "{}{}/".format(main_domain, shorten_link)
        formated_expiration_time = utils.format_string_to_readable_datetime(expiration_time)

        return Response(data={
            "shorten_url": shorten_url,
            "expiration_time": formated_expiration_time
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs).data
        return self.render_json_result(response_data)


def redirect_to_original_url(request, shorten_link):

    shorten_link_obj = get_object_or_404(
        klass=shorten_Link_model.ShortLinkCreator,
        shorten_link=shorten_link
    )

    utils.add_to_redirect_items_field(shorten_link_obj)

    return redirect(shorten_link_obj.original_url)
