from django.urls import path
from . import views


app_name = "shorten_app"


urlpatterns = [
    path(
        route="create/",
        view=views.CreateShortenLink.as_view(),
        name="create_shorten_link"
    ),
]
