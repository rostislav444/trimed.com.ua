from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


def create_staticpages():
    from .models import PageContacts, PageAbout

    if not PageContacts.objects.first():
        page_constacts = PageContacts()
        page_constacts.save()

    if not PageAbout.objects.first():
        page_about = PageContacts()
        page_about.save()

class PagesConfig(AppConfig):
    name = 'apps.pages'
    verbose_name = _("Страницы")

    def ready(self):
        try: create_staticpages()
        except: pass
        

       
