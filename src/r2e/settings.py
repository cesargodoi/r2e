import os
import dynaconf  # noqa
from pathlib import Path

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  #

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # others apps
    "widget_tweaks",
    "django_bootstrap5",
    # apps
    "apps.accounts",
    "apps.base",
    "apps.center",
    "apps.person",
    "apps.event",
    "apps.register",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "r2e.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "r2e.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.parent / "www/static/"

STATICFILES_DIRS = (
    "src/apps/base/static",
    BASE_DIR.parent / "www/assets/",
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / "www/media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = "/event/list/"
LOGIN_URL = "/accounts/login/"

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

settings = dynaconf.DjangoDynaconf(
    __name__,
    ENVVAR_PREFIX="R2E",
    SETTINGS_FILE_FOR_DYNACONF="../settings.yaml",
    SECRETS_FOR_DYNACONF="../.secrets.yaml",
)  # noqa
