"""User model."""

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from src.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Default custom user model."""

    email = models.EmailField(_("Email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts.",
        ),
    )
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Meta options for User model."""

        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_created"]
        abstract = False

    def __str__(self) -> str:
        """Return email as string representation."""
        return self.email

    def clean(self):
        """Normalize email."""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns
        -------
             URL for user's detail view.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
