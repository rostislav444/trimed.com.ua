from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class DocumentsConfig(AppConfig):
    name = 'apps.documents'
    verbose_name = _("Документы")
