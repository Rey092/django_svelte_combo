"""URL configuration for a project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("src.adminlte.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

if "requests_tracker" in settings.INSTALLED_APPS:
    urlpatterns += [path("__requests_tracker__/", include("requests_tracker.urls"))]
