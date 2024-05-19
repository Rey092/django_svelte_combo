"""Unfold configuration."""

# from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _


class UnfoldConfig:
    """Unfold configuration."""

    # UNFOLD
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
    # UNFOLD = {
    #     "SITE_TITLE": "Адміністрування Django",
    #     "SITE_SYMBOL": "speed",  # symbol from icon set
    #     "SHOW_HISTORY": False,  # show/hide "History" button, default: True
    #     "SHOW_VIEW_ON_SITE": False,  # show/hide "View on site" button, default: True
    #     "COLORS": {
    #         "primary": {
    #             "50": "250 245 255",
    #             "100": "243 232 255",
    #             "200": "233 213 255",
    #             "300": "216 180 254",
    #             "400": "192 132 252",
    #             "500": "168 85 247",
    #             "600": "147 51 234",
    #             "700": "126 34 206",
    #             "800": "107 33 168",
    #             "900": "88 28 135",
    #             "950": "147 51 234",
    #         },
    #     },
    #     "EXTENSIONS": {
    #         "modeltranslation": {
    #             "flags": {
    #                 "en": "🇬🇧",
    #             },
    #         },
    #     },
    #     "SIDEBAR": {
    #         "show_search": False,  # Search in applications and models names
    #         "show_all_applications": False,
    # Dropdown with all applications and models
    #         "navigation": [
    #             {
    #                 "title": _("Навігація"),
    #                 "separator": True,  # Top border
    #                 "items": [
    #                     {
    #                         "title": _("Юзери"),
    #                         # Supported icon set: https://fonts.google.com/icons
    #                         "icon": "person",
    #                         "link": reverse_lazy("admin:users_user_changelist"),
    #                     },
    #                 ],
    #             },
    #             {
    #                 "title": _("Налаштування"),
    #                 "separator": True,
    #                 "items": [
    #                     {
    #                         "title": _("Періодичні завдання"),
    #                         "icon": "schedule",
    #                         "link": reverse_lazy(
    #                             "admin:django_celery_beat_periodictask_changelist",
    #                         ),
    #                     },
    #                 ],
    #             },
    #         ],
    #     },
    #     "TABS": [
    #         {
    #             "models": [
    #                 "django_celery_beat.periodictask",
    #                 "django_celery_results.taskresult",
    #                 "django_celery_beat.crontabschedule",
    #             ],
    #             "items": [
    #                 {
    #                     "title": _("Періодичні завдання"),
    #                     "link": reverse_lazy(
    #                         "admin:django_celery_beat_periodictask_changelist",
    #                     ),
    #                     "permission": lambda request: request.user.is_superuser,
    #                 },
    #                 {
    #                     "title": _("Результати завдань"),
    #                     "link": reverse_lazy(
    #                         "admin:django_celery_results_taskresult_changelist",
    #                     ),
    #                     "permission": lambda request: request.user.is_superuser,
    #                 },
    #                 {
    #                     "title": _("Розклади"),
    #                     "link": reverse_lazy(
    #                         "admin:django_celery_beat_crontabschedule_changelist",
    #                     ),
    #                     "permission": lambda request: request.user.is_superuser,
    #                 },
    #             ],
    #         },
    #     ],
    # }
