from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from apps.blog.models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'shop/blog/blog.html'
    context_object_name = 'blog_posts'
    ordering = ['-created']
    paginate_by = 12
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
  
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'shop/blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context