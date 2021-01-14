from django.shortcuts import render, redirect
from django.urls import reverse
from apps.catalogue.models import Product
from apps.shop.models import Banner, PopularCategories
from apps.blog.models import BlogPost
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json


def tg_msg(phone):
    chanel_id = "1289759082"
    api_key = "1484777515:AAE_30QEs0Jb7_3mymgK0TYdTY2oD_M4orc"
    msg = f"Консультация: {phone}\n"
    try:
        msg = urllib.parse.quote(msg)
        url = f"https://api.telegram.org/bot{api_key}/sendMessage?chat_id=-100{chanel_id}&text=" + msg
        contents = urllib.request.urlopen(url).read()
    except: 
        pass


def home(request, api=False):
    context = {
        'banners' : Banner.objects.all(),
        'popular_categories' : PopularCategories.objects.all(),
        'blog' : BlogPost.objects.all(),
        'offer' : {
            'sale' : Product.objects.all()[:24],
            'popular' : Product.objects.all()[:24]
        }
    } 

    if request.method == 'POST':
        body = json.loads(request.body.decode("utf8"))
        consultation = body.get('consulatation')
        tg_msg(consultation)
        if api:
            return JsonResponse({'message' : 'Мы скоро с Вами свяжемся'})
    return render(request, 'shop/home/home.html', context)