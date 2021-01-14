from django.contrib import admin
from apps.blog.models import BlogPost, BlogPostImages, BlogPostProduct


class BlogPostImagesInline(admin.TabularInline):
    model = BlogPostImages
    extra = 0

class BlogPostProductInline(admin.TabularInline):
    model = BlogPostProduct
    extra = 0

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    readonly_fields = ['view']
    list_display = ['name', 'created', 'view']
    inlines = [
        BlogPostProductInline,
        BlogPostImagesInline
    ]

