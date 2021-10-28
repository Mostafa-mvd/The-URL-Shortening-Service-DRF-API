from rest_registration.api.views import register

from rest_framework import status

from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse

from users import utils as users_utils


@require_http_methods(['GET', 'POST'])
def register_user(request):

    response = register(request)

    if (request.method == "POST" and
        response.status_code == status.HTTP_201_CREATED):

        registered_user_id = response.data["id"]
        users_utils.generate_user_secret_key(registered_user_id)
        
    return response
    

def get_totp_code(request):
    if request.user.is_authenticated:

        totp_code = users_utils.generate_totp_code(request.user)
    
        return JsonResponse(
            data={
                "totp_code": totp_code
            }
        )

    return JsonResponse(
        data={
            "Authentication Error": "You didn't log in"
        }
    )
