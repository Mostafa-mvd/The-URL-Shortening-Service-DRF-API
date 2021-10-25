from django.urls import path
from . import views


app_name = "shorten_app"


urlpatterns = [
    path(
        route="",
        view=views.CreateShortenLink.as_view(),
        name="shorten"
    ),
]
