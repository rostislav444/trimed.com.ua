from django.db import models
from apps.core.models import NameSlug
from apps.catalogue.models.models__product import Product
from django.utils.translation import ugettext, ugettext_lazy as _


class Attribute(NameSlug):
    name =  models.CharField(max_length=100, blank=False, verbose_name=_("Название"), unique=True)
    slug =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Иденитификатор"), editable=False)

    class Meta:
        verbose_name = _("Группа атрибутов")
        verbose_name_plural = _("Группы атрибутов")

    def __str__(self):
        return self.name


class AttributeValue(NameSlug):
    parent = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='values')
    name =   models.CharField(max_length=100, blank=False, verbose_name=_("Название"))
    slug =   models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Иденитификатор"), editable=False)
    full_slug = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("Иденитификатор"), editable=False)

    class Meta:
        verbose_name = _("Атрибут")
        verbose_name_plural = _("Атрибуты")
        unique_together = ['parent', 'name']

    def save(self, *args, **kwargs):
        super(AttributeValue, self).save(*args, **kwargs)
        self.full_slug = self.parent.slug + '__' + self.slug
        super(AttributeValue, self).save(*args, **kwargs)
    


class CategoryAttribute(models.Model):
    parent =         models.ForeignKey('catalogue.Category',  on_delete=models.CASCADE, related_name='attributes', verbose_name=_("Катгория"))
    attribute =      models.ForeignKey(Attribute,             on_delete=models.CASCADE, related_name='category',   verbose_name=_("Группа атрибутов"))
    attribute_pk =   models.PositiveIntegerField(default=0, editable=False)
    values =         models.ManyToManyField(AttributeValue,   through="CategoryAttributeValue")
    
        
    class Meta:
        unique_together = ['parent', 'attribute']
        verbose_name = _("Связь атрибутов с категрией")
        verbose_name_plural = _("Связи атрибутов с категриями")

    def __str__(self):
        return f'{self.parent.name} {self.attribute.name}'

    def replace_attrs_to_parent_category(self):
        ancestors = self.parent.get_ancestors()
        for ancestor in ancestors:
            attribute = ancestor.attributes.filter(attribute=self.attribute).first()
    
            if attribute:
                for self_product_attr in self.product_attrs.all():
                    product_attr = ProductAttribute.objects.filter(parent=self_product_attr.parent, attribute=attribute).first()
                    if product_attr:
                        for val in self_product_attr.value.all():
                            if val not in product_attr.value.all():
                                product_attr.value.add(val)
                    self_product_attr.delete()

    def save(self):
        self.replace_attrs_to_parent_category()
        super(CategoryAttribute, self).save()
        if self.attribute_pk != self.attribute.pk:
            self.category_values.all().delete()
            for value in self.attribute.values.all():
                self.values.add(value)
            self.attribute_pk = self.attribute.pk
            super(CategoryAttribute, self).save()

    @property
    def get_attributes_values(self):
        values = CategoryAttributeValue
        values = self.category_values.all().values_list('value', flat=True)
        return AttributeValue.objects.filter(pk__in=values)

    @property
    def get_values(self):
        return self.values.all()
        

class CategoryAttributeValue(models.Model):
    parent =    models.ForeignKey(CategoryAttribute,  on_delete=models.CASCADE, related_name='category_values', verbose_name=_("Связь атрибутов с категрией"))
    value =     models.ForeignKey(AttributeValue,     on_delete=models.CASCADE, related_name='category_values', verbose_name=_("Атрибут"))

    class Meta:
        unique_together = ['parent', 'value']

    def __str__(self):
        return f'{self.parent.parent.name} > {self.value.name}'

    @property
    def get_value(self):
        return value.value.name

    class Meta:
        verbose_name = _("Атрибут категрии")
        verbose_name_plural = _("Атрибуты категрий")
        unique_together = ['parent', 'value']


class ProductAttribute(models.Model):
    parent =    models.ForeignKey('catalogue.Product',    on_delete=models.CASCADE, related_name='product_attrs')
    attribute = models.ForeignKey(CategoryAttribute,      on_delete=models.CASCADE, related_name='product_attrs')
    value =     models.ManyToManyField(AttributeValue, blank=True, related_name='product_attrs')

    class Meta:
        ordering = ['-attribute__attribute__name']
        verbose_name = _("Атрибуты товара")
        verbose_name_plural = _("Атрибуты товаров")
        unique_together = ['parent', 'attribute']

    def __str__(self):
        return f"{self.parent.name} - {self.parent.code} | Атрибуты: {self.attribute.attribute.name} - {', '.join([value.name for value in self.value.all()])}"

    