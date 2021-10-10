"""import appconfig"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """config polls"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
