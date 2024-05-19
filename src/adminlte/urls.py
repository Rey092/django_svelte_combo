"""Adminlte urls."""

from django.urls import path

from src.adminlte.pages.about import AboutPageInertiaView
from src.adminlte.pages.home import HomePageInertiaView

urlpatterns = [
    path("", HomePageInertiaView.as_view(), name="home"),
    path("about/", AboutPageInertiaView.as_view(), name="home"),
]
