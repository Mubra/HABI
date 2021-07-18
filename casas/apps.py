from django.apps import AppConfig
from django.conf import settings

# pylint: disable=import-outside-toplevel, unused-import


class CasasAppConfig(AppConfig):
    name = 'casas'
    verbose_name = settings.PRODUCT_LONG_NAME
