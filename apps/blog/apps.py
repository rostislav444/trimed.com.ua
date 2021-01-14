from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _

class BlogConfig(AppConfig):
    name = 'apps.blog'
    verbose_name = _("Блог")

