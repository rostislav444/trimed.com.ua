from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class CommentsConfig(AppConfig):
    name = 'apps.comments'
    verbose_name = _("Комментарии")
