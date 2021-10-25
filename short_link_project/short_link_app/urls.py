from django.urls import path
from . import views


app_name = "shorten_app"


urlpatterns = [
    path(
        route="shorten_link/",
        view=views.CreateShortenLink.as_view(),
        name="create_shorten_link"
    ),
    path(
        route='<str:shorten_link>/',
        view=views.redirect_to_original_url,
        name="redirect_shorten_url"
    ),
]
