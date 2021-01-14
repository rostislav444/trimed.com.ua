from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _
from apps.core.models.models__images import Image
from apps.core.models.models__translation import Translation
from apps.core.models.models__abstract import NameSlug



class Banner(Translation, Image):
    title =  models.CharField(blank=True, null=True, max_length=500, verbose_name=_("Заголовок"))
    text =   models.TextField(blank=True, null=True, verbose_name=_("Заголовок"))
    link =   models.CharField(blank=True, null=True, max_length=500, verbose_name=_("Ссылка"))
    create = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Баннер')
        verbose_name_plural = _('Баннера')
    

class PopularCategories(Image):
    num = models.PositiveIntegerField(default=0, verbose_name=_("Порядок сортировки"))
    category = models.OneToOneField('catalogue.Category', on_delete=models.CASCADE, verbose_name=_("Категория"))

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = _('Популярная категория')
        verbose_name_plural = _('Популярные категории')
    

class Messages(models.Model):
    name =    models.CharField(max_length=255, verbose_name=_("Имя"))
    surname = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Фамилия"))
    email =   models.EmailField(verbose_name=_("Email"))
    phone =   models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Телефон"))
    text =    models.TextField(verbose_name=_("Сообщение"))
    create = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Сообщения')
        verbose_name_plural = _('Сообщения')
