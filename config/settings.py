"""
Django settings for a project.
"""
import os
from pathlib import Path
from configurations import Configuration, values
from django.utils.translation import gettext_lazy as _


# noinspection PyPep8Naming
class Base(Configuration):
    """Base configuration."""

    # Basic variables
    BASE_DIR = Path(__file__).resolve().parent.parent
    DOTENV = os.path.join(BASE_DIR, '.env')

    # Secrets and APY keys
    SECRET_KEY = values.SecretValue()
    API_KEY = values.Value('91011')

    # Security
    DEBUG = values.BooleanValue(True)
    ALLOWED_HOSTS = values.ListValue(['*'])

    # Application definitions
    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    THIRD_PARTY_APPS = [
        "allauth",
        "allauth.account",
        # "allauth.mfa",
        # "allauth.socialaccount",
        "django_extensions",
    ]
    LOCAL_APPS = [
        "src.core",
        "src.users",
        "src.adminlte"
    ]

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
        "allauth.account.middleware.AccountMiddleware",
    ]

    # Database: https://docs.djangoproject.com/en/5.0/ref/settings/#databases
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": values.Value(environ_name="POSTGRES_DB"),
            "USER": values.Value(environ_name="POSTGRES_USER"),
            "PASSWORD": values.Value(environ_name="POSTGRES_PASSWORD"),
            "HOST": values.Value(environ_name="POSTGRES_HOST"),
            "PORT": values.IntegerValue(environ_name="POSTGRES_PORT"),
            "ATOMIC_REQUESTS": values.BooleanValue(True, environ_name="POSTGRES_ATOMIC_REQUESTS"),
            "CONN_MAX_AGE": values.IntegerValue(60, environ_name="POSTGRES_CONN_MAX_AGE"),
        }
    }

    # Default primary key field type: https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Internationalization: https://docs.djangoproject.com/en/5.0/topics/i18n/
    USE_I18N = True
    USE_TZ = True
    LANGUAGE_CODE = 'en-us'
    LANGUAGES = [
        ('en', _('English')),
    ]
    LOCALE_PATHS = [
        os.path.join(BASE_DIR, "locale"),
    ]

    # Timezone
    TIME_ZONE = 'UTC'

    # Site ID
    SITE_ID = 1

    # URL configurations
    ROOT_URLCONF = values.Value('config.urls')
    ADMIN_URL = values.Value("admin/")
    ROSETTA_LOGIN_URL = f"/{ADMIN_URL}/login/"

    # Login URL: https://docs.djangoproject.com/en/dev/ref/settings/#login-url
    LOGIN_URL = "account_login"

    # Login redirect: https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
    LOGIN_REDIRECT_URL = values.Value("/")

    # Applications: https://docs.djangoproject.com/en/5.0/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'config.wsgi.application'

    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    ]

    # Password validation: https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]

    # Authentication: https://docs.djangoproject.com/en/5.0/ref/settings/#authentication-backends
    AUTHENTICATION_BACKENDS = [
        # Needed to log in by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",
        # `allauth` specific authentication methods, such as login by email
        "allauth.account.auth_backends.AuthenticationBackend",
    ]

    # User Model https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
    AUTH_USER_MODEL = "users.User"

    # https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
    # Force the `admin` sign in process to go through the `django-allauth` workflow
    DJANGO_ADMIN_FORCE_ALLAUTH = values.BooleanValue(False, environ="DJANGO_ADMIN_FORCE_ALLAUTH")

    # Static Root: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = str(BASE_DIR / "staticfiles")
    # Static Url: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = "/static/"
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

    # LOGGING
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # See https://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }

    # Redis
    REDIS_URL = values.Value("redis://localhost:6379/0", environ_name="REDIS_URL")

    # Cache: https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        'default': {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # Mimicing memcache behavior.
                # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
                "IGNORE_EXCEPTIONS": values.Value(False, environ_name="REDIS_IGNORE_EXCEPTIONS")
            },
        }
    }

    # Celery
    # ------------------------------------------------------------------------------
    if USE_TZ:
        # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
        CELERY_TIMEZONE = TIME_ZONE
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
    CELERY_BROKER_URL = values.Value(REDIS_URL, environ_name="CELERY_BROKER_URL")
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
    CELERY_RESULT_EXTENDED = True
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
    # https://github.com/celery/celery/pull/6122
    CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
    CELERY_RESULT_BACKEND_MAX_RETRIES = 10
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
    CELERY_ACCEPT_CONTENT = ["json"]
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
    CELERY_TASK_SERIALIZER = "json"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
    CELERY_RESULT_SERIALIZER = "json"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
    # TODO: set to whatever value is adequate in your circumstances
    CELERY_TASK_TIME_LIMIT = 5 * 60
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
    # TODO: set to whatever value is adequate in your circumstances
    CELERY_TASK_SOFT_TIME_LIMIT = 60
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
    CELERY_WORKER_SEND_TASK_EVENTS = True
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
    CELERY_TASK_SEND_SENT_EVENT = True

    # django-allauth
    # ------------------------------------------------------------------------------
    ACCOUNT_ALLOW_REGISTRATION = values.BooleanValue(True)
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

    # Superuser data
    SUPERUSER_EMAIL = values.Value()
    SUPERUSER_PASSWORD = values.Value()

    # Telegram (for logging)
    # ------------------------------------------------------------------------------
    TELEGRAM_TOKEN = TELEGRAM_LOGGING_TOKEN = values.Value(None, environ_name="TELEGRAM_LOGGING_TOKEN")
    TELEGRAM_LOGGING_CHAT = values.Value(None, environ_name="TELEGRAM_LOGGING_CHAT")
    TELEGRAM_LOGGING_EMIT_ON_DEBUG = values.Value(False, environ_name="TELEGRAM_LOGGING_EMIT_ON_DEBUG")

    @property
    def INSTALLED_APPS(self):
        """Combine all installed apps."""
        return self.DJANGO_APPS + self.THIRD_PARTY_APPS + self.LOCAL_APPS

    @property
    def TEMPLATES(self):
        return [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': self.TEMPLATES_DIRS,
                'APP_DIRS': self.TEMPLATES_APP_DIRS,
                'OPTIONS': {
                    'context_processors': [
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


class Local(Base):
    """Local configuration."""

    # Email backend: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = values.Value("django.core.mail.backends.console.EmailBackend")

    # django-debug-toolbar: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    THIRD_PARTY_APPS = Base.THIRD_PARTY_APPS + ["debug_toolbar"]
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE = Base.MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    # requests-tracker: https://pypi.org/project/requests-tracker/#install-the-package
    THIRD_PARTY_APPS = THIRD_PARTY_APPS + ["requests_tracker"]
    MIDDLEWARE = MIDDLEWARE + ["requests_tracker.middleware.requests_tracker_middleware"]

    # ips: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    USE_DOCKER = values.BooleanValue(False)
    if USE_DOCKER:
        import socket
        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

    # Celery propagation: https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
    CELERY_TASK_EAGER_PROPAGATES = True


class DockerLoggingMixin:
    """Docker logging mixin."""

    THIRD_PARTY_APPS = ["django_telegram_logging"]
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            },
        },
        "handlers": {
            "telegram": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "src.core.utils.telegram_logger.CustomTelegramHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "django.request": {
                "handlers": ["telegram"],
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


class Dev(DockerLoggingMixin, Base):
    """Development configuration."""

    # update apps
    THIRD_PARTY_APPS = Base.THIRD_PARTY_APPS + DockerLoggingMixin.THIRD_PARTY_APPS


class Prod(DockerLoggingMixin, Base):
    """Production configuration."""

    # update apps
    THIRD_PARTY_APPS = Base.THIRD_PARTY_APPS + DockerLoggingMixin.THIRD_PARTY_APPS

    # Security
    DEBUG = False

    # HTTP Security checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS = 518400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_PRELOAD = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
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
    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

    # Email: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    # Templates
    TEMPLATES_DEBUG = True

    # Media test: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = "http://media.testserver"
