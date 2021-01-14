from django.apps import apps
from django.db import models
from apps.core.models import OneFile
from apps.core.models import NameSlug, Translation
from django.utils.translation import ugettext, ugettext_lazy as _


class ProductCertificate(OneFile):
    CERTIFICATE_TYPE = [
        ('FDA', 'FDA'),
        ('CE', 'CE'),
        ('CHI', 'CHI'),
    ]

    name =    models.CharField(max_length=100, blank=False, choices=CERTIFICATE_TYPE, verbose_name=_("Тип сертфиката"))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="certificates")

    class Meta:
        ordering = ['-num']
        verbose_name = _('Сертификат')
        verbose_name_plural = _('Сертификаты')

    def update_product_attrs(self):
        Attribute =         apps.get_model(app_label='catalogue_filters', model_name='Attribute')
        AttributeValue =    apps.get_model(app_label='catalogue_filters', model_name='AttributeValue')
        CategoryAttribute = apps.get_model(app_label='catalogue_filters', model_name='CategoryAttribute')
        ProductAttribute =  apps.get_model(app_label='catalogue_filters', model_name='ProductAttribute') 

        # ATTR GROUP
        try: attr = Attribute.objects.get(name="Сертификат")
        except: 
            attr = Attribute(name="Сертификат")
            attr.save()
        # ATTR VALUE
        attr_values = []
        for certificate in self.product.certificates.all().distinct():
            # ATTR VALUE
            try: value = AttributeValue.objects.get(parent=attr, name=certificate.name)
            except: 
                value = AttributeValue(parent=attr, name=certificate.name)
                value.save()
            # if value.name == self.name:
            attr_values.append(value)
                
        # CATEGORY ATTR GROUP
        try: cat_attr = CategoryAttribute.objects.get(parent=self.product.category, attribute=attr)
        except:
            cat_attr = CategoryAttribute(parent=self.product.category, attribute=attr)
            cat_attr.save()
        cat_attr.values.add(*attr.values.all())
        super(CategoryAttribute, cat_attr).save()
        # CATEGORY ATTR VALUE
        try: prod_attr_val = ProductAttribute.objects.get(parent=self.product, attribute=cat_attr)
        except: 
            prod_attr_val = ProductAttribute(parent=self.product, attribute=cat_attr)
            prod_attr_val.save()
        prod_attr_val.value.set(attr_values)
        super(ProductAttribute, prod_attr_val).save()


    def save(self):
        super(ProductCertificate, self).save()
        self.update_product_attrs()

    def delete(self):
        super(ProductCertificate, self).delete()
        self.update_product_attrs()
        
    
        
    

class ProductDocuments(OneFile, Translation):
    CERTIFICATE_TYPE = [
        ('DESCRIPTION',  'Описание'),
        ('PRESENTATION', 'Презентация'),
        ('METHOD',       'Способ применения'),
    ]
    name =    models.CharField(max_length=100, blank=False, choices=CERTIFICATE_TYPE, verbose_name=_("Тип документа"))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="documents")

    class Meta:
        ordering = ['-num']
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')
    