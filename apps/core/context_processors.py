
from django.utils.translation import get_language as lang
from apps.core.models import Languages, MainData
from django.urls import translate_url
from django.contrib.sites.shortcuts import get_current_site
import datetime
from project import settings

def cur_time(request):
    time = datetime.datetime.now()
    return {'time' : time}

def main_data(request):
    return {'maindata' : MainData.objects.first()}

def language_change(request):
    languages = []
    current_lang = lang()
    scheme = 'https' if request.is_secure() else 'http'
    base_url = ''.join([scheme,'://', request.META['HTTP_HOST']])
    path = str(request.path).replace('/' + str(current_lang) + '/', '').split('/')
    path = '/'.join([p for p in path if len(p) > 0])

   
    for language in Languages.objects.all():
        params = [path]
        if settings.LANGUAGE_CODE != language.code: 
            params.insert(0, language.code)
        l = { 
            'code' : language.code,
            'path' : base_url + '/' + '/'.join(params),
            'active' : True if language.code == current_lang else False,
        }
        languages.append(l)
    return {'languages' : languages, 'current_lang':current_lang}