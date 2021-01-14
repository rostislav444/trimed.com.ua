from django.shortcuts import render, redirect
from django.urls import reverse
from apps.catalogue.models import Product, ProductCharacteristics
from apps.catalogue_filters.models import Attribute
from apps.shop.comparelist import CompareList
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from collections import OrderedDict



class ComparisonViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    template_name = 'shop/comparison/comparison.html'
    context = {}

    def get(self, request):
        compare = CompareList(request)
        ids = [int(pk) for pk in compare]
        products = Product.objects.filter(pk__in=ids)
        attrs = Attribute.objects.filter(category__product_attrs__parent__in=products).distinct().order_by('name')
        chars = ProductCharacteristics.objects.filter(parent__in=products)
        
        data = [{'key' : attr.name, 'values' : [] } for attr in attrs]

        for product in products:
            for attr_n, attr in enumerate(attrs):
                product_attr = product.product_attrs.filter(attribute__attribute=attr).first()
                if product_attr:
                    values = product_attr.value.all().values_list('name', flat=True)
                    value = ', '.join(values)
                else:
                    value = '-'
                data[attr_n]['values'].append(value)
        
        return render(request, self.template_name, {'products':products,'data' : data})

    def add(self, request):
        products_id = request.data.get('product_id')
        compare = CompareList(request)
        compare.add(products_id)
        return redirect(reverse('shop:comparison'))

    def clear(self, request):
        products_id = request.data.get('product_id')
        compare = CompareList(request)
        compare.clear()
        return redirect(request.META.get('HTTP_REFERER'))

    def remove(self, request):
        products_id = request.data.get('product_id')
        compare = CompareList(request)
        compare.remove(products_id)
        return redirect(request.META.get('HTTP_REFERER'))