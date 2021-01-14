from django.urls import re_path, path, include
from apps.blog import views

app_name = 'blog'


urlpatterns = [
    path('',            views.BlogPostListView.as_view(), name='blog'),
    path('page-<page>', views.BlogPostListView.as_view(), name='blog'),
    path('<int:year>/<int:month>/<int:day>/<slug>/', views.BlogPostDetailView.as_view(), name='post'),
]

