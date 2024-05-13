"""Django settings for a project."""

from pathlib import Path

from configurations import Configuration
from configurations import values
from django.utils.translation import gettext_lazy as _

from config.allauth import AllauthConfig
from config.celery.config import CeleryConfig
from config.celery.config import CeleryLocalConfig
from config.celery.schedule import CeleryScheduleConfig
from config.svelte.config import InertiaConfig
from config.telegram.config import TelegramConfig
from config.unfold import UnfoldConfig


# noinspection PyPep8Naming
class Base(
    TelegramConfig,
    InertiaConfig,
    AllauthConfig,
    UnfoldConfig,
    CeleryScheduleConfig,
    CeleryConfig,
    Configuration,
):
    """Base configuration."""

    # Basic variables
    BASE_DIR = Path(__file__).resolve().parent.parent
    DOTENV = BASE_DIR / ".env"
    BACKEND_URL = values.Value("http://localhost:8000")
    PROJECT_TITLE = values.Value("My Awesome Project")

    # Secrets and APY keys
    SECRET_KEY = values.SecretValue()
    API_KEY = values.Value("91011")

    # Security
    DEBUG = values.BooleanValue(default=True)
    ALLOWED_HOSTS = values.ListValue(["*"])

    # Application definitions
    DJANGO_APPS = [
        "unfold",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    THIRD_PARTY_APPS = [
        *AllauthConfig.ALLAUTH_APPS,
        "django_extensions",
        "django_cleanup.apps.CleanupConfig",
        "django_celery_beat",
        "django_celery_results",
        "django_telegram_logging",
        *InertiaConfig.INERTIA_INSTALLED_APPS,
    ]
    LOCAL_APPS = ["src.core", "src.users", "src.adminlte"]

    # Templates
    TEMPLATES_DIRS = []
    TEMPLATES_APP_DIRS = True
    TEMPLATES_DEBUG = True

    # Middleware
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        # TODO: remove whitenoise?
        # "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        *AllauthConfig.ALLAUTH_MIDDLEWARE,
        *InertiaConfig.INERTIA_MIDDLEWARE,
    ]

    # Default primary key field type: https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Internationalization: https://docs.djangoproject.com/en/5.0/topics/i18n/
    USE_I18N = True
    USE_TZ = True
    LANGUAGE_CODE = "en-us"
    LANGUAGES = [
        ("en", _("English")),
    ]
    LOCALE_PATHS = [
        BASE_DIR / "locale",
    ]

    # Timezone
    TIME_ZONE = "UTC"

    # Site ID
    SITE_ID = 1

    # URL configurations
    ROOT_URLCONF = values.Value("config.urls")
    ADMIN_URL = values.Value("admin/")
    ROSETTA_LOGIN_URL = f"/{ADMIN_URL}/login/"

    # Login URL: https://docs.djangoproject.com/en/dev/ref/settings/#login-url
    LOGIN_URL = "account_login"

    # Login redirect: https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
    LOGIN_REDIRECT_URL = values.Value("/")

    # Applications: https://docs.djangoproject.com/en/5.0/ref/settings/#wsgi-application
    WSGI_APPLICATION = "config.wsgi.application"

    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    ]

    # Password validation: https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Authentication: https://docs.djangoproject.com/en/5.0/ref/settings/#authentication-backends
    AUTHENTICATION_BACKENDS = [
        # Needed to log in by username in Django admin
        "django.contrib.auth.backends.ModelBackend",
        *AllauthConfig.ALLAUTH_AUTHENTICATION_BACKENDS,
    ]

    # User Model https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
    AUTH_USER_MODEL = "users.User"

    # Static Root: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = str(BASE_DIR / "staticfiles")
    # Static Url: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = "/static/"
    # Static Dirs: https://docs.djangoproject.com/en/dev/ref/settings/#staticfiles-dirs
    STATICFILES_DIRS = [
        BASE_DIR / "static",
        # *SvelteConfig.SVELTE_STATICFILES_DIRS,
    ]
    # Static Finders: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    ]

    # Media Root: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = str(BASE_DIR / "media")
    # Media Url: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = "/media/"

    # Email backend: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = values.Value("django.core.mail.backends.smtp.EmailBackend")
    # Email timeout: https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
    EMAIL_TIMEOUT = 5

    # Redis
    REDIS_URL = values.Value("redis://localhost:6379/0", environ_prefix="")

    # Superuser data
    SUPERUSER_EMAIL = values.Value()
    SUPERUSER_PASSWORD = values.Value()

    # Logging: https://docs.djangoproject.com/en/5.0/topics/logging/
    @property
    def LOGGING(self):  # noqa: N802
        """Logging configuration."""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "%(levelname)s %(asctime)s %(module)s "
                    "%(process)d %(thread)d %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                },
                "telegram": {
                    "level": "ERROR",
                    "class": "config.telegram.handler.CustomTelegramHandler",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            },
            "loggers": {
                "django.request": {
                    "handlers": ["console", "telegram"],
                    "level": "ERROR",
                    "propagate": True,
                },
                "django.security.DisallowedHost": {
                    "level": "ERROR",
                    "handlers": ["console", "telegram"],
                    "propagate": True,
                },
            },
        }

    @property
    def INSTALLED_APPS(self):  # noqa: N802
        """Combine all installed apps."""
        return [
            *self.DJANGO_APPS,
            *self.THIRD_PARTY_APPS,
            *self.LOCAL_APPS,
        ]

    @property
    def DATABASES(self):  # noqa: N802
        """Database configuration.

        https://docs.djangoproject.com/en/5.0/ref/settings/#databases
        """
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": values.Value(environ_name="POSTGRES_DB", environ_prefix=None),
                "USER": values.Value(environ_name="POSTGRES_USER", environ_prefix=None),
                "PASSWORD": values.Value(
                    environ_name="POSTGRES_PASSWORD", environ_prefix=None
                ),
                "HOST": values.Value(environ_name="POSTGRES_HOST", environ_prefix=None),
                "PORT": values.IntegerValue(
                    environ_name="POSTGRES_PORT", environ_prefix=None
                ),
                "ATOMIC_REQUESTS": values.BooleanValue(
                    default=True,
                    environ_name="POSTGRES_ATOMIC_REQUESTS",
                    environ_prefix=None,
                ),
                "CONN_MAX_AGE": values.IntegerValue(
                    default=60,
                    environ_name="POSTGRES_CONN_MAX_AGE",
                    environ_prefix=None,
                ),
            },
        }

    def CACHES(self):  # noqa: N802
        """Cache configuration.

        https://docs.djangoproject.com/en/dev/ref/settings/#caches
        """
        return {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": self.REDIS_URL,
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    # Mimicing memcache behavior.
                    # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
                    "IGNORE_EXCEPTIONS": values.Value(
                        default=False,
                        environ_name="REDIS_IGNORE_EXCEPTIONS",
                    ),
                },
            },
        }

    @property
    def TEMPLATES(self):  # noqa: N802
        """Templates configuration."""
        return [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": self.TEMPLATES_DIRS,
                "APP_DIRS": self.TEMPLATES_APP_DIRS,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.template.context_processors.static",
                        "django.contrib.messages.context_processors.messages",
                    ],
                    "debug": self.TEMPLATES_DEBUG,
                },
            },
        ]


# noinspection PyUnreachableCode
class Local(CeleryLocalConfig, Base):
    """Local configuration."""

    # Email backend: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = values.Value("django.core.mail.backends.console.EmailBackend")

    # TODO: check all those debug toolbars
    # django-debug-toolbar: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    THIRD_PARTY_APPS = [*Base.THIRD_PARTY_APPS, "debug_toolbar"]
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE = [
        *Base.MIDDLEWARE,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    # requests-tracker: https://pypi.org/project/requests-tracker/#install-the-package
    THIRD_PARTY_APPS = [*THIRD_PARTY_APPS, "requests_tracker"]
    MIDDLEWARE = [
        *MIDDLEWARE,
        "requests_tracker.middleware.requests_tracker_middleware",
    ]

    # ips: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    USE_DOCKER = values.BooleanValue(default=False)
    if USE_DOCKER:
        import socket

        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]


class Dev(Base):
    """Development configuration."""


class Prod(Base):
    """Production configuration."""

    # Security
    DEBUG = False

    # HTTP Security checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS = 518400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(default=True)
    SECURE_HSTS_PRELOAD = values.BooleanValue(default=True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(default=True)
    SECURE_SSL_REDIRECT = values.BooleanValue(default=True)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # Default from Email: https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
    DEFAULT_FROM_EMAIL = values.Value("My Awesome Project <noreply@example.com>")
    # Server Email: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
    SERVER_EMAIL = values.Value(DEFAULT_FROM_EMAIL)
    # Email Subject Prefix: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
    EMAIL_SUBJECT_PREFIX = values.Value("[My Awesome Project] ")


class Test(Base):
    """Test configuration."""

    # Speed up tests: https://docs.djangoproject.com/en/5.0/topics/testing/overview/#speeding-up-the-tests
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    TEST_RUNNER = "django.test.runner.DiscoverRunner"

    # Email: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    # Templates
    TEMPLATES_DEBUG = True

    # Media test: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = "http://media.testserver"
