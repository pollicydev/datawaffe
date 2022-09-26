from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rrap.organizations"

    def ready(self):
        try:
            import rrap.organizations.signals  # noqa F401
        except ImportError:
            pass
