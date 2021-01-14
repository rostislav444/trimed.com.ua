from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class CatalogueFiltersConfig(AppConfig):
    name = 'apps.catalogue_filters'
    verbose_name = _("Фильтры товаров")
