from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from unfold.forms import AdminPasswordChangeForm

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User
from ..core.admins.base import BaseAdmin

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(BaseAdmin):
    actions = []
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("date_created",)}),
    )
    list_display = ["email", "is_superuser"]
    readonly_fields = ["date_created"]
    search_fields = ["email"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    change_password_form = AdminPasswordChangeForm
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
