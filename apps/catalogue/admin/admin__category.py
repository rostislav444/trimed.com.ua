from django.contrib import admin
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms import TextInput, Textarea
from apps.core.admin_globals import InlineObjectLink, AdminImagePreview
from apps.catalogue_filters.models import CategoryAttribute
from apps.catalogue.models import *
from apps.catalogue.forms import CategoryAttributeForm,  CategoryAttributeFormSet


FORMFIELD_OVERRIDES = {
    models.PositiveIntegerField: {'widget': TextInput(attrs={'size':'30'})},
    models.CharField: {'widget': TextInput(attrs={'size':'30'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':61})},
}


class CategoryAttributeinline(admin.TabularInline, InlineObjectLink):
    model =   CategoryAttribute
    form =    CategoryAttributeForm
    formset = CategoryAttributeFormSet
    fields = ['attribute','link']
    readonly_fields = ['link']
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryAttributeinline,]
    list_display = ['name','sm_price','md_price','bg_price']
    list_editable = ['sm_price','md_price','bg_price']
    formfield_overrides = FORMFIELD_OVERRIDES
    

