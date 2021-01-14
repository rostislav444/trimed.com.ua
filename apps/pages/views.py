from django.shortcuts import render
from django.views.generic.detail import DetailView
from apps.pages.models import PageContacts, PageAbout, PageGroup, Page
from apps.shop.forms import MessagesForm
from django.forms.models import model_to_dict

class PageDetailView(DetailView):
    model = Page
    template_name = 'shop/pages/page__static.html'
    context_object_name = 'page'


def page_about(request):
    
    return render(request, 'shop/pages/page__about.html', {
        'page' : PageAbout.objects.first(),
    })


def page_constacts(request):
    form_valid = False
    if request.method == 'POST':
        form = MessagesForm(data=request.POST)
        if form.is_valid():
            form.save()
            form_valid = True
    else:
        data = {}
        if request.user.is_authenticated:
            user = request.user
            data = model_to_dict(user)
        form = MessagesForm(initial=data)
    return render(request, 'shop/pages/page__contacts.html', {
        'page' : PageContacts.objects.first(),
        'form' : form, 
        'form_valid' : form_valid,
    })