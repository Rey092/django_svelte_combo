"""
Django settings for a project.
"""
import os
from pathlib import Path
from configurations import Configuration, values


class StaticMixin:
    """Mixin for static files configuration."""

    # Static files: https://docs.djangoproject.com/en/4.2/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = 'staticfiles'


# noinspection PyPep8Naming
class Base(StaticMixin, Configuration):
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

    # Default primary key field type: https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Application definitions
    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    THIRD_PARTY_APPS = []
    LOCAL_APPS = []

    # Project routes
    ROOT_URLCONF = values.Value('config.urls')

    # Templates
    TEMPLATES_DIRS = []
    TEMPLATES_APP_DIRS = True
    TEMPLATES_DEBUG = True

    # Middleware
    MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            "CONN_MAX_AGE": values.IntegerValue(0, environ_name="POSTGRES_CONN_MAX_AGE"),
        }
    }

    # Internationalization: https://docs.djangoproject.com/en/5.0/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True
    SITE_ID = 1
    LOCALE_PATHS = [
        str(BASE_DIR / "locale")
    ]

    # Applications: https://docs.djangoproject.com/en/5.0/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'config.wsgi.application'

    # Password validation: https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]

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
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                    "debug": self.TEMPLATES_DEBUG,
                },
            },
        ]


class Local(Base):
    """Local configuration."""


class Dev(Base):
    """Development configuration."""


class Prod(Base):
    """Production configuration."""

    # Security
    DEBUG = False

    # HTTP Security checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

    # Middleware
    MIDDLEWARE = Base.MIDDLEWARE + ['django.middleware.security.SecurityMiddleware']


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
