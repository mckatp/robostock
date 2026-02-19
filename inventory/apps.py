import os
from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        if os.environ.get("CREATE_SUPERUSER") == "1":
            from django.db.models.signals import post_migrate
            post_migrate.connect(_create_superuser, sender=self)


def _create_superuser(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="murshidbbg").exists():
        User.objects.create_superuser(
            username="murshidbbg",
            email="bloombergmurshid@gmail.com",
            password="Murshid@BBG",
        )
