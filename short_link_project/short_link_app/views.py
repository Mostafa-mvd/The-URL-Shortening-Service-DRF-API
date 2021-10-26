from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer

from users import utils as users_utils

from django.shortcuts import get_object_or_404, redirect

from . import (utils as shortening_link_utils,
                serializers as shortening_link_serializers, 
               models as shortening_Link_models)


class CreateShortenLink(generics.CreateAPIView):
    serializer_class = shortening_link_serializers.ShortenLinkSerializer
    model = shortening_Link_models.ShortLinkCreator

    def render_json_result(self, response_data):
        shorten_link = response_data["result_link"]
        expiration_time = response_data["expiration_time"]
        is_url_private = response_data["is_shorten_url_private"]

        shortened_url = shortening_link_utils.concatenate_domain_with_path(
            self.request, shorten_link)

        formated_expiration_time = shortening_link_utils.format_string_to_readable_datetime(
            expiration_time)

        return Response(data={
            "shorten_url": shortened_url,
            "expiration_time": formated_expiration_time,
            "is_url_private": is_url_private
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        if (request.user.is_anonymous and
            request.POST.get("is_shorten_url_private", None)):

            login_url = shortening_link_utils.concatenate_domain_with_path(
                self.request, "users_urls:login")

            register_url = shortening_link_utils.concatenate_domain_with_path(
                self.request, "users_urls:register")

            return Response(data={
                "authentication": "You are not authenticated for using private url",
                "login_url": login_url,
                "register_url": register_url
                },
                status=status.HTTP_403_FORBIDDEN
            )

        response_data = super().post(request, *args, **kwargs).data

        return self.render_json_result(response_data)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def redirect_to_original_url(request, shorten_link, otp_code=None):

    shorten_link_obj = get_object_or_404(
        klass=shortening_Link_models.ShortLinkCreator,
        shorten_link=shorten_link
    )

    if shorten_link_obj.is_shorten_url_private:
        if not request.user.is_authenticated:

            login_url = shortening_link_utils.concatenate_domain_with_path(
                request, "users_urls:login")

            return Response(data={
                "OTP ERROR": "Your url is private , you have to login first",
                "login_url": login_url
                }, content_type="application/json"
            )
        if otp_code:
            if not users_utils.is_otp_code_valid(otp_code, request.user):
                return Response(data={
                    "OTP ERROR": "otp code is not valid"
                    }, content_type="application/json"
                )
        else:
            otp_generator_url = shortening_link_utils.concatenate_domain_with_path(
                request, "users_urls:generate_otp_code")

            return Response(data={
                "OTP ERROR": "Your url is private , set access otp code first",
                "otp_generator": otp_generator_url
                }, content_type="application/json"
            )

    shortening_link_utils.add_to_redirect_items_field(
        shorten_link_obj)

    return redirect(
        shorten_link_obj.original_url)
