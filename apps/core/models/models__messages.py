from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext, ugettext_lazy as _


class Message(models.Model):
    subject =    models.CharField(blank=False,  max_length=255, verbose_name=_("Тема письма"))
    date =       models.DateTimeField(auto_now=True, verbose_name=_("Время отправки"))
    first_name = models.CharField(blank=False, max_length=255, verbose_name=_("Имя"))
    email =      models.CharField(blank=False, max_length=255, verbose_name=_("Email"))
    phone =      models.CharField(blank=True,  max_length=255, verbose_name=_("Телефон"))
    text =       RichTextField(blank=False,    verbose_name=_("Текст письма"))
    
    class Meta:
        verbose_name = _('Сообщения')
        verbose_name_plural = _('Сообщения')