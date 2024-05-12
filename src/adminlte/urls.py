"""Adminlte urls."""

from django.urls import path

from src.adminlte.pages.home import HomePageInertiaView

urlpatterns = [
    path("", HomePageInertiaView.as_view(), name="home"),
]
