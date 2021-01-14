from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user.models import *
from apps.catalogue.models import Category
from apps.user.forms import UserSubscriptionForm
from django.contrib.auth.models import Group


admin.site.unregister(Group)


# WISHLIST
class WishlistInline(admin.TabularInline):
    model = Wishlist
    extra = 0


# ADRESS
class UserAdressInline(admin.TabularInline):
    model = UserAdress
    extra = 0


class UserSubscriptonInline(admin.TabularInline):
    model = UserSubscripton
    form = UserSubscriptionForm
    extra = 0


class UserAdressChosenInline(admin.TabularInline):
    model = UserAdressChosen

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(UserAdressChosenInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'adress':
            if request._object:
                field.queryset = field.queryset.filter(parent=request._object)
            else: 
                field.queryset = field.queryset.none()
        return field
 


# NEWPOST
class UserNPInline(admin.TabularInline):
    model  = UserNP
    extra = 0

class UserNPChosenInline(admin.TabularInline):
    model = UserNPChosen

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(UserNPChosenInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'adress':
            if request._object:
                field.queryset = field.queryset.filter(parent=request._object)
            else: 
                field.queryset = field.queryset.none()
        return field


class UserCompanyInline(admin.TabularInline):
    model  = UserCompany
    extra = 0


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [
        UserSubscriptonInline,
        UserNPChosenInline,
        UserNPInline,
        UserAdressChosenInline,
        UserAdressInline, 
        UserCompanyInline,
        WishlistInline
    ]
    list_display = (
        'email','email_confirmed','phone','phone_confirmed','name','surname','patronymic','created','is_active'
    )
    
    list_filter = (
        'is_admin', 'is_active'
    )
    fieldsets = (
        (None, {'fields': ('name','surname','patronymic','birthday')}),
        # ('Организация', {'fields': ('organization','position',)}),
        ('Contacts',    {'fields': ('email','email_confirmed','phone','phone_confirmed','password')}),
        ('Permissions', {'fields': ('is_admin', 'was_active','is_active','is_manager','is_client')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ['-created']
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        request._object = obj
        return super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
   
