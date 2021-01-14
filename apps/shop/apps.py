from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _
import os

def load_products():
    from apps.catalogue.models import Product, ProductImages, Category
    from project import settings
    import PIL
    import json

    category_fiedls = [field.name for field in Category()._meta.fields if field.name not in ['parent'] ]
    product_fiedls =  [field.name for field in Product()._meta.fields if field.name not in [] ]


    with open(settings.MEDIA_ROOT + 'db.json', 'r') as json_file:
        data = json.load(json_file)

        for item in data:
            model = item.get('model')

            if model in ['catalogue.productimages']:

                fields = item.get('fields')
                pk = item.get('pk')
                product = Product.objects.get(pk=fields.get('product'))
                # print(settings.MEDIA_URL + fields.get('image_l'))
                path = settings.MEDIA_ROOT + fields.get('image_l')
                # print(os.path.exists(path))
               
                image = ProductImages(pk=pk, image=path, product=product)
                image.save()
            # if model in ['catalogue.product']:
            #     fields = item.get('fields')
            #     pk = item.get('pk')
            #     try: 
            #         Product.objects.get(pk=pk)
            #     except:
            #         product = Product(pk=pk) 
            #         for k, v in fields.items():
            #             if k in product_fiedls:
            #                 if k == 'category':
            #                     v = Category.objects.get(pk=v)
            #                 setattr(product, k,v)
            #         product.save()
                
            # if model in ['catalogue.category']:
            #     pk = item.get('pk')

            #     fields = item.get('fields')
            #     try: 
            #         Category.objects.get(pk=pk)
            #     except:
            #         category = Category(pk=pk) 
            #         for k, v in fields.items():
            #             if k in category_fiedls:
            #                 setattr(category, k,v)
            #         category.save()


class ShopConfig(AppConfig):
    name = 'apps.shop'
    verbose_name = _("Магазин")

    def ready(self):
        # load_products()
        pass
        
                        
                    
                    
        

        