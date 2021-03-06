"""short_link_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from short_link_app import views
import debug_toolbar


urlpatterns = [
    path(
        'admin/', 
        admin.site.urls
    ),
    path(
        "api/v1/shortening_link/",
        include('short_link_app.urls',
                namespace="shortening_link_urls"
        ),
    ),
    path(
        "api/v1/users/",
        include('users.urls',
                namespace="users_urls"
        ),
    ),
    url(
        r'^(?P<token>[\w-]{8,18})/',
        include([
            url(
                regex=r'^$',
                view=views.redirector,
                name="redirect_to_public_url"),

            url(regex=r'^(?P<otp_code>\d+)/$',
                view=views.redirector,
                name="redirect_to_private_url"),
        ])
    ),
    path('__debug__/', include(debug_toolbar.urls)),
]
