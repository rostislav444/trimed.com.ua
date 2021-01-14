from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q, Prefetch, Case, When, Count, Value, F,  ExpressionWrapper, Sum
from django.db.models.functions import Round
from django.db.models import IntegerField, BooleanField, CharField, TextField
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import RawSQL
from django.core.paginator import Paginator
from django.views.generic import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from apps.catalogue.models import Product, Category
from apps.catalogue_filters.models import Attribute, AttributeValue, CategoryAttribute, CategoryAttributeValue, ProductAttribute
from apps.catalogue.serilaizers import CategorySerializer, AttributeSerializer, AttributeValueSerializer, ProductSerializer
import json
import time
import math


class Catalogue(View):
    context = {'sort_by' : ['price_asc','price_dsc','newest','popularity']}
    attrvalues = []
    attrkeys = []

    # GET ALL CHILD CATEGORIES
    def get_categories(self, category):
        if category: 
            return category.get_descendants(include_self=True)
        return Category.objects.all()
                   
    # ALL ATRIBUTES IN CATEGORIES
    def get_attrs(self, category, params_attr=None, params=None, products_excluded=None, products_filtered=None):
        all_categories = Category.objects.all()
        excluded__pks = products_excluded.values_list('pk', flat=True)
        attr_values = AttributeValue.objects.distinct().filter(
            category_values__parent__parent__in = category.get_family() if category else all_categories,
            product_attrs__parent__category__in = category.get_descendants(include_self=True) if category else all_categories
        )
        
        attr_values =  attr_values.annotate(
            count=Count(
                'product_attrs__parent',  
                filter=Q(
                    product_attrs__parent__in=products_filtered,
                ), 
                output_field=IntegerField(), 
                distinct=True
            ),
        )
        if params_attr:
            attr_values = attr_values.annotate(
                selected=Case(When(params_attr, then=Value(True)), default=Value(False), output_field=BooleanField(),),
            )
        attrs = Attribute.objects.distinct().filter(values__in=attr_values).prefetch_related(
            Prefetch('values', attr_values)
        )
        return attrs



    # GET SELECTED ATTRIBUTES FROM URL PARAMS
    def get_selected_attrs(self, atributes=None):
        if atributes:
            params_price = {}
            params_attr, params  = Q(), {}
            for attr in atributes.split('/'):
                try: key, value = attr.split('=')
                except: continue
                value = value.split(',')
                if key == 'price':
                    params_price['price_ua__gte'] = int(value[0])
                    params_price['price_ua__lte'] = int(value[1])
                else:
                    print(key, value)
                    params_attr |= Q(parent__slug=key, slug__in=value)
                    params[key] = value
            return params_attr, params_price, params
        else:
            return None, {}, {}


    # FILTER PRODUCTS BU ATRIBUTES
    def filter_products_attrs(self, products, params):
        values = []
        keys = []

        if params:
            for key, value in params.items():
                if key in ['price_ua__gte', 'price_ua__lte']:
                    products = products.filter(**{key : value})
                else:
                    products = products.filter(
                        product_attrs__attribute__attribute__slug = key, 
                        product_attrs__value__slug__in = value,
                    )
                    for val in value:
                        values.append(key + '__' + val) 
                    keys.append(key) 
            
            products = products.distinct()
            self.attrvalues = values
            self.attrkeys = keys
        return products

    # SORT PRODUCTS
    def get_sorted(self, products, sort):
        order_by = {
            'newest'    : '-update',
            'popular' : '-update',
            'price_asc' : 'price',
            'price_dsc' : '-price',
        }
        if sort:
            return products.order_by(order_by[sort])
        return products.order_by(order_by['newest'])


    # PRICE RANGE
    def set_price_range(self, params, context, products):
        lst_price_product = products.order_by('price').first()
        hst_price_product = products.order_by('-price').first()
        context['min_price'] =  int(lst_price_product.get_price_ua if lst_price_product else 0)
        context['max_price'] =  math.ceil(hst_price_product .get_price_ua if hst_price_product  else 1)
        gte = params['price_ua__gte'] if 'price_ua__gte' in params.keys() else context['min_price']
        lte = params['price_ua__lte'] if 'price_ua__lte' in params.keys() else context['max_price']
        context['price__gte'] = gte if gte >= context['min_price'] else context['min_price']
        context['price__lte'] = lte if lte <= context['max_price'] else context['max_price']
        return context


    def pagination(self, products, kwargs, page):
        pagination = Paginator(list(products), 8).page(page)
        page_current = pagination.number
        page_total = pagination.paginator.num_pages
        self.context['pages'] = {
            'current' : page_current,
            'total' :   page_total,
        }
        self.context['pages']['middle'] = {
            'pages' : [],
            'max' : page_total - 2
        }
        for i in range(page_current - 2, page_current + 2):
            if i > 1 and i < page_total:
                self.context['pages']['middle']['last'] = i
                if len(self.context['pages']['middle']['pages']) == 0:
                    self.context['pages']['middle']['first'] = i
                url = reverse(
                    'shop:catalogue', kwargs=dict(
                        list(kwargs.items()) + [('page', i)]
                    )
                )
                self.context['pages']['middle']['pages'].append({'num' : i, 'url' : url})
       


        self.context['pages']['more'] = reverse(
            'shop:catalogue', kwargs=dict(
                list(kwargs.items()) + [('page', pagination.next_page_number())]
            )
        ) if pagination.has_next() else None 
        
        # FIRST PAGE
        self.context['pages']['first'] = reverse(
            'shop:catalogue', kwargs=kwargs
        )
        # LAST PAGE
        self.context['pages']['last'] = reverse(
            'shop:catalogue', kwargs=dict(
                list(kwargs.items()) + [('page', pagination.paginator.num_pages)]
            )
        )
        # PREVIOUS PAGE
        self.context['pages']['previous'] = reverse(
            'shop:catalogue', kwargs=dict(
                list(kwargs.items()) + [('page', pagination.previous_page_number())]
            )
        ) if pagination.has_previous() else None
        # NEXT PAGE
        self.context['pages']['next'] = reverse(
            'shop:catalogue', kwargs=dict(
                list(kwargs.items()) + [('page', pagination.next_page_number())]
            )
        ) if pagination.has_next() else None
        self.context['pagination'] = render_to_string('shop/catalogue/catalogue__pagination.html', self.context)
        return pagination.object_list
        

    def filter_price(self, products, params_price):
        if params_price:
            products = products.filter(**params_price)
        return products



    def set_context(self, category, sort, atributes, page, per_page=24):
        context = self.context
        page = int(page) if page else 1
        kwargs = {
            'category' : category,
            'atributes' : atributes,
            'sort' : sort,
        }
        delete = [key for key in kwargs if kwargs[key] == None] 
        for key in delete: del kwargs[key] 

        # FIlter by attrs
        params_attr, params_price, params = self.get_selected_attrs(atributes)

        # Filter by categories
        category = Category.objects.filter(slug=category).first()
        categories = self.get_categories(category)
        category_products_all = Product.objects.filter(category__in=categories)
        category_products_filtered = self.filter_products_attrs(category_products_all, params)
        category_products_filtered__pks = category_products_filtered.values_list('pk', flat=True)
        category_products_excluded = category_products_all.exclude(pk__in=category_products_filtered__pks)
       
        attrs = self.get_attrs(category, params_attr, params, category_products_excluded, category_products_filtered)
        attrs_serialized = AttributeSerializer(attrs, many=True, context={
            'products': category_products_filtered , 
            'category' : category,
            'params':params,
        }).data
        
        context =  self.set_price_range(params_price, context, category_products_filtered)
        products = self.filter_price(category_products_filtered, params_price)
        products = self.get_sorted(products, sort)

        context['category'] =   category
        context['categories'] = categories
        context['products'] =   self.pagination(products, kwargs, page)
        context['attributes'] = json.loads(json.dumps(attrs_serialized))
        return context


    def get(self, request, category=None, sort=None, atributes=None, page=None, per_page=None):
        context = self.set_context(category, sort, atributes, page)
        return render(request, 'shop/catalogue/catalogue.html', context)


    def post(self, request, category=None, sort=None, atributes=None, page=None, per_page=None):
        more = request.GET.get('more')
        context = self.set_context(category, sort, atributes, page)
        context['request'] = request
        products = render_to_string('shop/catalogue/catalogue__product__list.html', context)
        attributes = render_to_string('shop/catalogue/catalogue__filters.html', context)
        
        print(more)


        return JsonResponse({
            'products' : products, 
            'pagination' : context['pagination'],
            'attributes' : attributes,
            'more' : context['pages']['more']
        })