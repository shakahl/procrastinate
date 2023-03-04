import os

SECRET_KEY = "test"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("PGDATABASE", "procrastinate"),
        "TEST": {
            "NAME": os.environ.get("PGDATABASE", "procrastinate") + "_django_test"
        },
    },
}

INSTALLED_APPS = [
    "procrastinate.contrib.django",
    "tests.acceptance.django_app",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
