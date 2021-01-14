from django.shortcuts import render
from django.template.loader import render_to_string
from apps.shop.watchlist import WatchList
from django.http import JsonResponse
import json

def watchlist(request):
    print('WATCHLIST')
    watchlist = WatchList(request)
    
    template = 'shop/additions/watchlist/watchlist__products.html'
    html = render_to_string(template, {'products' : watchlist.data()})
    response = {'html' : html, 'length' : len(watchlist.data())}
    return JsonResponse(response)