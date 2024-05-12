"""Adminlte urls."""

from django.urls import path

from src.adminlte.views import HomePageInertiaView

urlpatterns = [
    path("", HomePageInertiaView.as_view(), name="home"),
]
