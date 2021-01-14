from django.db import models
from django.urls import reverse
from apps.core.models.models__images import Image
from apps.core.models.models__translation import Translation
from apps.core.models.models__abstract import NameSlug
from ckeditor.fields import RichTextField
from django.utils.translation import gettext as _


class PageContacts(Translation):
    text =  RichTextField( null=True, blank=True, verbose_name=_("Текст"))
    phone = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Номер телефона'))
    email = models.EmailField(max_length=500, null=True, blank=True, verbose_name=_('Email'))
    
    class Meta:
        verbose_name = _("Страница: Котнакты")
        verbose_name_plural = _("Страница: Котнакты")

    def __str__(self):
        return self.title

    @property
    def title(self):
        return  _("Наши контакты")




class PageAbout(Translation):
    text = RichTextField(null=True, blank=True, verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Страница: О нас")
        verbose_name_plural = _("Страница: О нас")
    
    def __str__(self):
        return self.title

    @property
    def title(self):
        return _("О нас")



class PageGroup(Translation, NameSlug):
    class Meta:
        verbose_name = _("Статичная страница | Группа")
        verbose_name_plural = _("Статичные страницы | Группы")


class Page(Translation, Image, NameSlug):
    parent = models.ForeignKey(PageGroup, on_delete=models.CASCADE, verbose_name=_("Группа"), related_name="pages")
    text =   RichTextField(verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Статичная страница")
        verbose_name_plural = _("Статичные страницы")

    def get_absolute_url(self):
        return reverse('pages:page', kwargs={'slug':self.slug})