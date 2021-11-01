from django.urls import path

from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView

from . import views

app_name = "users_app"


urlpatterns = [
    path(
        route="registration/",
        view=RegisterView.as_view(),
        name="register"
    ),
    path(
        route="login/",
        view=LoginView.as_view(),
        name="login"
    ),
    path(
        route="logout/",
        view=LogoutView.as_view(),
        name="logout"
    ),
    path(
        route="generate_otp/",
        view=views.GenerateOTPCode.as_view(),
        name="generate_otp_code"
    ),
]
