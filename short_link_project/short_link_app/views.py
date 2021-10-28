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
    serializer_class = shortening_link_serializers.ShorteningLinkSerializer
    model = shortening_Link_models.ShortLink

    def represent_result(self, response_data):

        return Response(data={
            "short_url": response_data["short_url"],
            'created_time': response_data['created_time'],
            "expiration_time": response_data['expiration_time'],
            "private": response_data["is_private"]
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

        return self.represent_result(response_data)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def redirect_to_original_url(request, token, otp_code=None):

    short_link = get_object_or_404(
        klass=shortening_Link_models.ShortLink,
        token=token)

    if short_link.is_private:
        if not request.user.is_authenticated:

            login_url = shortening_link_utils.concatenate_domain_with_path(
                request, "users_urls:login")

            return Response(data={
                "OTP ERROR": "Your url is private , you have to login first",
                "login_url": login_url
                }, content_type="application/json")

        if otp_code:
            if not users_utils.is_totp_code_valid(otp_code, request.user):
                return Response(data={
                    "OTP ERROR": "otp code is not valid, after 120 seconds try again"
                    }, content_type="application/json")
        else:
            otp_generator_url = shortening_link_utils.concatenate_domain_with_path(
                request, "users_urls:generate_otp_code")

            return Response(data={
                "OTP ERROR": "Your url is private , set access otp code first",
                "otp_generator": otp_generator_url
                }, content_type="application/json")

    short_link.add_to_times_of_redirected_field()

    return redirect(short_link.original_url)
