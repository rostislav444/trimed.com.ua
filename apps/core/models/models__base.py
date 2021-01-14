from django.db import models
from apps.core.models import Translation, NameSlug
from apps.core.functions.function__filefield import FileField
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext, ugettext_lazy as _


class MainData(Translation):
    logo =      FileField(upload_to="file_codes", blank=True, null=True, verbose_name=_("Логотип сайта"))
    favicon =   FileField(upload_to="file_codes", blank=True, null=True, verbose_name=_("Fav icon"))

    phone =     models.CharField(max_length=255,  blank=True, null=True, verbose_name=_("Телефон"))
    email =     models.EmailField(max_length=255, blank=True, null=True, verbose_name=_("E-mail"))
    adress =    models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Адрес"))

    meta_title = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Мета тег Titile (Домашней страницы)"))
    meta_descr = models.TextField(max_length=500, blank=True, null=True, verbose_name=_("Мета тег Description (Домашней страницы)"))
    seo_text =   RichTextField(blank=True, null=True, verbose_name=_("SEO текст (Домашней страницы)"))


    class Meta:
        verbose_name = _('Основная информация')
        verbose_name_plural = _('Основная информация')
