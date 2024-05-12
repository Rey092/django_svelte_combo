"""Allauth configuration settings."""

from configurations import values


class AllauthConfig:
    """Allauth configuration settings.

    https://docs.allauth.org/en/latest/account/configuration.html
    """

    ACCOUNT_ALLOW_REGISTRATION = values.BooleanValue(default=True)
    # https://docs.allauth.org/en/latest/account/configuration.html
    ACCOUNT_AUTHENTICATION_METHOD = "email"
    # https://docs.allauth.org/en/latest/account/configuration.html
    ACCOUNT_EMAIL_REQUIRED = True
    # https://docs.allauth.org/en/latest/account/configuration.html
    ACCOUNT_USERNAME_REQUIRED = False
    # https://docs.allauth.org/en/latest/account/configuration.html
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    # https://docs.allauth.org/en/latest/account/configuration.html
    ACCOUNT_EMAIL_VERIFICATION = "none"
    # https://docs.allauth.org/en/latest/account/configuration.html
    ACCOUNT_ADAPTER = "src.users.adapters.AccountAdapter"
    # https://docs.allauth.org/en/latest/account/forms.html
    ACCOUNT_FORMS = {"signup": "src.users.forms.UserSignupForm"}
    # https://docs.allauth.org/en/latest/socialaccount/configuration.html
    SOCIALACCOUNT_ADAPTER = "src.users.adapters.SocialAccountAdapter"
    # https://docs.allauth.org/en/latest/socialaccount/configuration.html
    SOCIALACCOUNT_FORMS = {"signup": "src.users.forms.UserSocialSignupForm"}
