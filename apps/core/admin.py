from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import *


@admin.register(Message)
class MessageAdmin(SingleModelAdmin):
    pass

@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    pass


@admin.register(MainData)
class MainDataAdmin(admin.ModelAdmin):
    pass
