from django.urls import re_path, path, include
from apps.shop import views

app_name = 'shop'


urlpatterns = [
    path('watchlist',          views.watchlist, name="watchlist"),
    path('comparison/',        views.ComparisonViewSet.as_view({'get':'get'}),     name="comparison"),
    path('comparison/add/',    views.ComparisonViewSet.as_view({'post':'add'}),    name="comparison-add"),
    path('comparison/remove/', views.ComparisonViewSet.as_view({'post':'remove'}), name="comparison-remove"),
    path('comparison/clear/',  views.ComparisonViewSet.as_view({'get':'clear'}),   name="comparison-clear"),

    re_path(
        r'''^product/(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/comment/(?P<comment_id>[0-9]+)''',   
        views.ProductPage.as_view({'get':'comment_reply','post':'comment_reply'}),   
        name="comment_reply"
    ),
    re_path(
        r'''^product/(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/question/(?P<question_id>[0-9]+)''',   
        views.ProductPage.as_view({'get':'question_reply','post':'question_reply'}),   
        name="question_reply"
    ),

    # path('question/<question_id>', views.ProductPage.as_view({'get':'question_reply'}),  name="question_reply"),
    
    re_path(
        r'''^catalogue/?'''
        r'''(?:\/(?P<category>[\w-]+))?/?'''
        r'''(?:\/page/(?P<page>[\d+]+))?/?'''
        r'''(?:\/(?P<atributes>([\w-]+(=[,\w-]*))?(((\/[\w-]+(=[,\w-]*))?)*)))?/?'''
        r'''(?:\/sort/(?P<sort>price_asc|price_dsc|newest|popular))?/?'''
        r'''(?:\/per_page/(?P<per_page>[\d+]+))?/?$''',
        views.Catalogue.as_view(), 
        name="catalogue"
    ),
    re_path(
        r'''^product/(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''?(?:\/(?P<page>characteristics|comments|questions|certificates|))?/?$''',
        views.ProductPage.as_view({'get':'page'}), 
        name="product"
    ),
    re_path(
        r'''^product/(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''?(?:\/(?P<page>comment_form))?/?$''',
        views.ProductPage.as_view({'post':'comment_form'}), 
        name="comment_form"
    ),
     re_path(
        r'''^product/(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''?(?:\/(?P<page>question_form))?/?$''',
        views.ProductPage.as_view({'post':'question_form'}), 
        name="question_form"
    ),
    path('', views.home, name="home"),
    re_path(r"^(?P<api>api)/",views.home, name='home'),
]

