from apps.catalogue.models import Product
from project import settings


class CompareList(object):
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get(settings.COMPARE_SESSION_ID)
        if not compare:
            compare = self.session[settings.COMPARE_SESSION_ID] = []
        self.compare = compare

    def __iter__(self):
        for item in self.compare:
            yield item

    def save(self):
        self.session.modified = True

    def add(self, product_id):
        id = int(product_id)
        compare = self.compare
        if id in compare:
            compare.remove(id)
        compare.insert(0, id)
        self.compare = compare
        self.save()
        return self.data()

    def remove(self, product_id):
        n = None
        compare = self.compare
        for n, product in enumerate(compare):
            if n == product_id:
                break
        del self.compare[n]
        self.save()

    def clear(self):
        del self.session[settings.COMPARE_SESSION_ID]
        self.save()
   
    def data(self):
        exclude, product_list = [], []
        products = Product.objects.filter(pk__in=self.compare)
        for product_id in self.compare:
            try:
                product_list.append(products.get(pk=int(product_id))) 
            except:
                exclude.append(product_id)
        return product_list