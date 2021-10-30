from rest_framework import status

from django.http.response import JsonResponse

from dj_rest_auth.registration.views import RegisterView

from users import utils as users_utils


class UserRegistrationView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if (request.method == "POST" and
                response.status_code == status.HTTP_201_CREATED):

            registered_user_pk = response.data["user"]['pk']
            users_utils.generate_user_secret_key(registered_user_pk)

        return response
    

def get_totp_code(request):
    if request.user.is_authenticated:

        totp_code = users_utils.generate_totp_code(request.user)
    
        return JsonResponse(
            data={
                "totp_code": totp_code,
                "ttl in minutes": users_utils.get_otp_code_ttl() / 60
            }
        )

    return JsonResponse(
        data={
            "Authentication Error": "You didn't log in"
        }
    )
