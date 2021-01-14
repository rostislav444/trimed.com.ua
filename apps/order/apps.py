from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class OrderConfig(AppConfig):
    name = 'apps.order'
    verbose_name=_("Заказы")
