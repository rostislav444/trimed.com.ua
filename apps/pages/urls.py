from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.pages import views


app_name = 'pages'


urlpatterns = [
    path('about',    views.page_about, name='about'),
    path('contacts', views.page_constacts, name='contacts'),
    path('<slug>',   views.PageDetailView.as_view(), name='page')

   
]
