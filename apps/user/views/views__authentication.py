from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.views import View
from apps.user.models import CustomUser
from apps.catalogue.models import Product
from apps.user.forms import LoginForm, RegistrationForm



class AuthenticationView(View):
    template_name = 'shop/user/authentication.html'
    context = {}
    
    def set_context_data(self, request, page=None):
        request = request.POST if request.method == "POST" else None
        self.context = {
            'forms' : {
                'login' : LoginForm(data=request),
                'registration' : RegistrationForm(data=request),
            },
            'page' : page
        }

    def get(self, request, page=None, api=None):
        
      
        self.set_context_data(request, page)
        self.context['redirect'] = request.GET.get('redirect')
        return render(request, self.template_name, self.context)

    def post(self, request, page=None, api=None):
        self.set_context_data(request, page)
        self.context['errors'] = None
        url_redirect = request.GET.get('redirect')
        
        # LOGIN
        if page == 'login' or page == None:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = CustomUser.objects.get(email=form.cleaned_data['username'])
                login(request, user)
                if url_redirect:
                    return redirect(url_redirect)
                return redirect(reverse('user:user_data'))
        # REGISTER
        elif page == 'registration':
            form = RegistrationForm(data=request.POST)
            if form.is_valid():
                user = CustomUser.objects.get(email=form.cleaned_data['email'])
                form.save()
                login(request, user)
                if url_redirect:
                    return redirect(url_redirect)
                return redirect(reverse('user:user_data'))
        return render(request, self.template_name, self.context)


