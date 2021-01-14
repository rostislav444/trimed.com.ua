from django.urls import include, path, re_path
from apps.user import views

app_name = 'user'

wishlist = [
    path('',        views.WishlistViewsSet.as_view({'get': 'data'}),    name='wishlist'),
    path('add/',    views.WishlistViewsSet.as_view({'post': 'add'}),    name='wishlist_add'),
    path('remove/', views.WishlistViewsSet.as_view({'post': 'remove'}), name='wishlist_remove'),
]

authentication = [
    path('',  views.AuthenticationView.as_view(), name='authentication'),
    re_path(
        r"^(?P<page>login|registration|)/?((?P<api>api)/)?$", 
        views.AuthenticationView.as_view(), 
        name='authentication'
    ),
]

profile = [
    path('',                 views.user_data,            name='user_data'),
    path('orders/',          views.user_orders,          name='user_orders'),
    path('wishlist/',        views.user_wishlist,        name='user_wishlist'),
    path('company/',         views.user_company,         name='user_company'),
    path('subscribe/',       views.user_subscribe,       name='user_subscribe'),
    path('comments/',        views.user_comments,        name='user_comments'),
    path('questions/',       views.user_questions,       name='user_questions'),
    path('logout/',          views.user_logout,          name='user_logout'),
    path('password_change/', views.user_password_change, name='user_password_change'),
    
]

urlpatterns = [
    path('whishlist/',  include(wishlist)),
    path('authntication/', include(authentication)),
    path('profile/', include(profile)),
]
