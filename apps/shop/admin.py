from django.contrib import admin
from .models import Banner, PopularCategories, Messages


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


@admin.register(PopularCategories)
class PopularCategoriesAdmin(admin.ModelAdmin):
    pass




@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'surname', 'phone', 'email', 'create'
    ]