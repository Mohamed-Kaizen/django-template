"""Django base settings for {{cookiecutter.project_name}} project."""
import pathlib
from datetime import timedelta

from better_exceptions.integrations.django import skip_errors_filter
from decouple import Csv, config
from dj_database_url import parse as db_url
from django.utils.translation import gettext_lazy as _
{% if cookiecutter.use_sentry == 'y' -%}
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
{%- endif %}

# General
# ------------------------------------------------------------------------------
BASE_DIR = pathlib.Path().absolute()

TEMPLATES_DIR = [BASE_DIR.joinpath("templates")]

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = config("DEBUG", cast=bool)

ADMIN_URL = config("ADMIN_URL", cast=str, default="admin/")

# using python-decouple to hide the SECRET_KEY
SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(str))

SITE_ID = 1

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "{{cookiecutter.project_slug}}.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "{{cookiecutter.project_slug}}.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
]
THIRD_PARTY_APPS = [
    "axes",
    "django_filters",
    {% if cookiecutter.app_type != 'plain django' -%}"corsheaders",{%- endif %}
    {% if cookiecutter.production_storage != 'filesystem' -%}"storages",{%- endif %}
    {% if cookiecutter.use_django_dbbackup == 'y' -%}"dbbackup",{%- endif %}
    {% if cookiecutter.background_task == 'django-q' -%}"django_q", {%- endif %}
    {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' or cookiecutter.app_type == "django rest framework with firebase auth" -%}
    "rest_framework",
    "drf_spectacular",
    {%- endif %}
    {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' -%}
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "dj_rest_auth",
    {%- endif %}
]

LOCAL_APPS = ["users.apps.UsersConfig"]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    {% if cookiecutter.app_type != 'plain django' -%}"corsheaders.middleware.CorsMiddleware",  # django-cors-headers{%- endif %}
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "better_exceptions.integrations.django.BetterExceptionsMiddleware",
    "axes.middleware.AxesMiddleware",  # django-axes
]

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
    {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' -%}"allauth.account.auth_backends.AuthenticationBackend",{%- endif %}
)

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.CustomUser"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "/"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
{% if cookiecutter.password_hashing_algorithm == 'Argon2' -%}
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django  # noqa: B950
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
{% elif cookiecutter.password_hashing_algorithm == 'bcrypt' -%}
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-bcrypt-with-django  # noqa: B950
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
{%- else %}

    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
{%- endif %}
]


# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: B950
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {
        "NAME": "pwned_passwords_django.validators.PwnedPasswordsValidator",
        "OPTIONS": {
            "error_message": "Oh no — pwned! This password has been seen "
            "%(amount)d times before",
            "help_message": "Your password can't be a commonly used password.",
        },
    },
]

# STATIC (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS  # noqa: B950
STATICFILES_DIRS = [BASE_DIR.joinpath("static")]

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = BASE_DIR.joinpath("static_root")

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR.joinpath("media")

# ADMIN
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("{{cookiecutter.author_name}}", "{{cookiecutter.email}}")]

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Internationalization
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "{{cookiecutter.timezone}}"

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [BASE_DIR.joinpath("local")]

LANGUAGES = (("en", _("English")), ("ar", _("Arabic")))

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND  # noqa: B950
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": TEMPLATES_DIR,
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors  # noqa: B950
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "users.context_processors.from_settings",
            ],
        },
    }
]

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = not DEBUG

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = not DEBUG

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = not DEBUG


# Email
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config("EMAIL_USER", cast=str)
    EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD", cast=str)

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": config("DATABASE_URL", cast=db_url, default="sqlite:///db.sqlite3")
}

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {"rich": {"datefmt": "[%B %d, %X, %Y]"}},
    'filters': {
        'skip_errors': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_errors_filter,
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['skip_errors'],
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
        }
    },
    'loggers': {
        'django': {
            'handlers': [
                'console',
            ],
        }
    }
}

{% if cookiecutter.use_redis == 'y' -%}
# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", cast=str),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
{%- endif %}

# Third-Party Settings
# whitenoise
# ------------------------------------------------------------------------------
if DEBUG:
    INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# django-debug-toolbar
# ------------------------------------------------------------------------------
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config  # noqa: B950
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TEMPLATE_CONTEXT": True}

    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips  # noqa: B950
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

    # displaying panels for django debug
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]

# django-axes
# ------------------------------------------------------------------------------
AXES_COOLOFF_TIME = timedelta(minutes=60) if not DEBUG else timedelta(minutes=5)
AXES_FAILURE_LIMIT = 5
AXES_USE_USER_AGENT = True

{% if cookiecutter.production_storage != 'filesystem' -%}
# django-storages
# ------------------------------------------------------------------------------
if not DEBUG:
    {% if cookiecutter.production_storage == 'Dropbox' -%}
    DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"

    DROPBOX_OAUTH2_TOKEN = config("DROPBOX_OAUTH2_TOKEN", cast=str)

    DROPBOX_ROOT_PATH = "media"

    {% else -%}
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", cast=str)

    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)

    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", cast=str, default="media")

    {% if cookiecutter.production_storage == 'MinIO' -%}AWS_S3_ENDPOINT_URL = config("MinIO_URL", cast=str){%- endif %}

    {%- endif %}

{%- endif %}


{% if cookiecutter.use_sentry == 'y' -%}
# sentry
# ------------------------------------------------------------------------------
sentry_sdk.init(
    dsn=config("SENTRY_DSN", cast=str),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
{%- endif %}

{% if cookiecutter.background_task == 'django-q' -%}
# django-q
# ------------------------------------------------------------------------------
Q_CLUSTER = {
    'name': '{{cookiecutter.project_slug}}',
    'workers': 4,
    'retry': 5,
    'timeout': 4,
    {% if cookiecutter.use_redis == 'y' -%}'django_redis': 'default'{%- endif %}
}
{%- endif %}

{% if cookiecutter.use_django_dbbackup == 'y' -%}
# django-dbbackup
# ------------------------------------------------------------------------------
{% if cookiecutter.production_storage == 'filesystem' -%}
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/my/backup/dir/'}
{% elif cookiecutter.production_storage == 'Dropbox' -%}
if not DEBUG:
    DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
    DBBACKUP_STORAGE_OPTIONS = {
        'oauth2_access_token': DROPBOX_OAUTH2_TOKEN,
        "root_path": DROPBOX_ROOT_PATH
    }
{% else -%}
if not DEBUG:
    DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DBBACKUP_STORAGE_OPTIONS = {
        'access_key': AWS_ACCESS_KEY_ID,
        'secret_key': AWS_SECRET_ACCESS_KEY,
        'bucket_name': AWS_STORAGE_BUCKET_NAME,
        'default_acl': 'private',
       "location": "backups",
        {% if cookiecutter.production_storage == 'MinIO' -%}"endpoint_url": AWS_S3_ENDPOINT_URL{%- endif %}
    }
{%- endif %}

{%- endif %}

{% if cookiecutter.app_type != 'plain django' -%}
# django-cors-headers
# ------------------------------------------------------------------------------
# https://github.com/adamchainz/django-cors-headers#cors_allow_all_origins
CORS_ALLOW_ALL_ORIGINS = DEBUG
if not DEBUG:
    CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv(str))
{%- endif %}

{% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' or cookiecutter.app_type == "django rest framework with firebase auth" -%}
# djangorestframework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' -%}"dj_rest_auth.jwt_auth.JWTCookieAuthentication",{%- endif %}
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
{%- endif %}

{% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' -%}
# djangorestframework-simplejwt
# ------------------------------------------------------------------------------
SIMPLE_JWT = {
    "USER_ID_FIELD": "id",
}

# dj-rest-auth
# ------------------------------------------------------------------------------
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

ACCOUNT_EMAIL_REQUIRED = True

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "users.serializers.UserDetailsSerializer",
    "JWT_SERIALIZER": "users.serializers.JWTSerializer",
}

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "users.serializers.CustomRegisterSerializer",
}
ACCOUNT_ADAPTER = "users.adapter.CustomAccountAdapter"

OLD_PASSWORD_FIELD_ENABLED = True

LOGOUT_ON_PASSWORD_CHANGE = True
{%- endif %}

# Your settings...
# ------------------------------------------------------------------------------

if DEBUG:

    ENVIRONMENT_NAME = _("Dev")

    ENVIRONMENT_COLOR = "red"

else:

    ENVIRONMENT_NAME = _("Production")

    ENVIRONMENT_COLOR = "green"

CUSTOM_RESERVED_NAMES = []
