from django.urls import path
from . import views
from rest_registration.api.views import login, logout

app_name = "users_app"


urlpatterns = [
    path(
        route="register/",
        view=views.register_user,
        name="register"
    ),
    path(
        route="login/",
        view=login,
        name="login"
    ),
    path(
        route="logout/",
        view=logout,
        name="logout"
    ),
    path(
        route="generate_otp/",
        view=views.get_totp_code,
        name="generate_otp_code"
    ),
]
