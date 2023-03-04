import django

from .utils import connector_params

__all__ = ["connector_params"]

if django.VERSION < (3, 2):
    default_app_config = "procrastinate.contrib.django.apps.ProcrastinateConfig"
