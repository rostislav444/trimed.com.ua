from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.order import views


app_name = 'order'


urlpatterns = [
    

    path('', views.OrderViewSet.as_view({'get':'data', 'post':'data'}), name='order'),
    re_path(
        r"^(?P<delivery>newpost|curier)/",
        views.OrderViewSet.as_view({'get':'data', 'post':'data'}), 
        name='order'
    ),
    re_path(
        r"^api/(?P<delivery>newpost|curier)/",
        views.OrderViewSet.as_view({'post':'api'}), 
        name='order_api'
    ),
    path('success/', views.order_success, name='success')
    
    
   
]
