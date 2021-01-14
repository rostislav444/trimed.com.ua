from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from apps.core.models.models__images import Image
from apps.core.models.models__translation import Translation
from apps.core.models.models__abstract import NameSlug
from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
from django.utils.translation import ugettext, ugettext_lazy as _


class BlogPost(NameSlug, Translation, Image):
    description = RichTextField(blank=True, verbose_name=_("Описание"))
    generate_anotation =   models.BooleanField(default=True, verbose_name=_("Заполнть анотацию из описания"))
    anotation =   models.TextField(blank=True, null=True, verbose_name=_("Анотация"))
    created =     models.DateTimeField(default=now)
    view =        models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))

    class Meta:
        ordering = ['-created']
        verbose_name = _('Пост')
        verbose_name_plural =  _('Посты')

    def save(self):
        if self.generate_anotation:
            self.anotation = BeautifulSoup(self.description).text[:500]
            self.generate_anotation = False
        super(BlogPost, self).save()

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={
            'slug' : self.slug, 'year' : self.created.year, 'month' : self.created.month, 'day' : self.created.day
        })


class BlogPostImages(Image):
    parent = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ['-num']
        verbose_name = _('Картинка')
        verbose_name_plural = _('Картинки')


class BlogPostProduct(models.Model):
    parent =   models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="products")
    product =  models.ForeignKey('catalogue.Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['parent', 'product']]
        verbose_name = _('Товар в посте')
        verbose_name_plural = _('Товары в посте')
