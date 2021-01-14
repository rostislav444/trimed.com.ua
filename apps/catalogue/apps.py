from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class CatalogueConfig(AppConfig):
    name = 'apps.catalogue'
    verbose_name = _("Каталог")
