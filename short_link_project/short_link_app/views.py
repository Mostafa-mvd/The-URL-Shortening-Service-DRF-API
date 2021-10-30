from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

from . import (utils as shortening_link_utils,
                serializers as shortening_link_serializers, 
               models as shortening_Link_models)

from users import utils as users_utils


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
            request.POST.get("is_private", None)):

            return Response(data={
                "authentication": "You are not authenticated for using private url",
                },
                status=status.HTTP_403_FORBIDDEN
            )

        response_data = super().post(request, *args, **kwargs).data

        return self.represent_result(response_data)


@cache_page(shortening_link_utils.get_cache_ttl())
@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def redirector(request, token, otp_code=None):

    short_link = get_object_or_404(
        klass=shortening_Link_models.ShortLink,
        token=token)

    if short_link.is_private:
        if not request.user.is_authenticated:
            return JsonResponse(data={
                "OTP ERROR": "Your url is private , you have to login first",
                })

        if otp_code:
            if not users_utils.is_totp_code_valid(otp_code, request.user):
                return JsonResponse(data={
                    "OTP ERROR": "otp code is not valid"
                    })
        else:
            return JsonResponse(data={
                "OTP ERROR": "Your url is private , set access otp code first"
                })

    short_link.add_to_times_of_redirected_field()

    return redirect(short_link.original_url)
