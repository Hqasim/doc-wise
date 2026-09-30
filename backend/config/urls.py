from django.conf import settings
from django.urls import path

from core.api import api

urlpatterns = [path("api/", api.urls)]

if settings.DEBUG:
    from django.contrib import admin

    urlpatterns.append(path("admin/", admin.site.urls))
