from django.contrib import admin
from . import models as shortener_links_models


admin.site.register([
    shortener_links_models.ShortLinkCreator
])
