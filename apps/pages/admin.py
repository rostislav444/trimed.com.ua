from django.contrib import admin
from apps.pages.models import PageContacts, PageAbout, PageGroup, Page
from singlemodeladmin import SingleModelAdmin

@admin.register(PageContacts)
class PageContactsAdmin(SingleModelAdmin):
    pass

@admin.register(PageAbout)
class PageAboutAdmin(SingleModelAdmin):
    pass

class PageInline(admin.TabularInline):
    model = Page
    fields = [
        'image','name','text'
    ]

@admin.register(PageGroup)
class PageGroupAdmin(admin.ModelAdmin):
    inlines = [
        PageInline
    ]

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
