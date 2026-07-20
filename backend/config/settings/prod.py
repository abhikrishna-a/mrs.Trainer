from .base import *  # noqa: F401,F403
from decouple import config

DEBUG = False

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="aptitude_platform"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
        "CONN_MAX_AGE": 600,
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(",") if config("CSRF_TRUSTED_ORIGINS", default="") else []

CORS_ALLOW_ALL_ORIGINS = False

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
