from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bitso_summary.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import bitso_summary.users.signals  # noqa F401
        except ImportError:
            pass
