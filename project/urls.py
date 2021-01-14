from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path, include
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView


urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain'), name='robots'),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type='application/xml'), name='sitemap'),
]


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    # Modules
    path('ckeditor/',  include('ckeditor_uploader.urls')),
    path('api-auth/',  include('rest_framework.urls')),
    # Apps
    path('blog/',      include('apps.blog.urls')),
    path('cart/',      include('apps.cart.urls')),
    path('search/',    include('apps.search.urls')),
    path('user/',      include('apps.user.urls')),
    path('whoosale/',  include('apps.catalogue.urls')),
    path('documents',  include('apps.documents.urls')),
    path('comments/',  include('apps.comments.urls')),
    path('order/',     include('apps.order.urls')),  
    path('pages/',     include('apps.pages.urls')),
    path('',           include('apps.shop.urls')),
    # I18N
    path('i18n/',      include('django.conf.urls.i18n')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

