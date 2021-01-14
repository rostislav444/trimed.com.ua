from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from apps.user.models import Wishlist, CustomUser, UserAdress
from apps.catalogue.models import Product
from apps.user.forms.forms__user_data import *


@login_required()
def user_data(request, name=None):
    context = {}
    user=request.user
    forms = {
        'main' :           UserDataMainForm, 
        'contacts' :       UserDataConstactsForm,
        'adress_chosen' :  UserAdressChosenFormSetFactory,
        'adress' :         UserAdressFromSet,
    }

    if request.method == 'POST':
        key = request.GET.get('form')
        if key in forms.keys():
            form = forms[key](data=request.POST, instance=user)
            if form.is_valid():
                form.save()

    for key in forms.keys():
        form = forms[key]
        forms[key] = form(instance=user)
            
    context['forms'] = forms
    return render(request, 'shop/user/profile/profile__userdata.html', context)

@login_required()
def user_orders(request):
    return render(request, 'shop/user/profile/profile__orders.html')

@login_required()
def user_wishlist(request):
    return render(request, 'shop/user/profile/profile__wishlist.html')

@login_required()
def user_company(request):
    if request.method == 'POST':
        formset = UserCompanyFormSet(data=request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
        else:
            print('not valid')
    else:
        formset = UserCompanyFormSet(instance=request.user)

    return render(request, 'shop/user/profile/profile__company.html', {'formset' : formset})

@login_required()
def user_subscribe(request):
    if request.method == 'POST':
        formset = UserSubscriptionFormSet(data=request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
        else:
            print('not valid')
    else:
        formset = UserSubscriptionFormSet(instance=request.user)
    return render(request, 'shop/user/profile/profile__subscribe.html', {'formset' : formset})

@login_required()
def user_comments(request):
    return render(request, 'shop/user/profile/profile__comments.html')

@login_required()
def user_questions(request):
    return render(request, 'shop/user/profile/profile__questions.html')

@login_required()
def user_password_change(request):
    done = False
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('user:user_password_change'))
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request, 'shop/user/profile/profile__passwordchange.html', {'form':form, 'done' : done})

@login_required()
def user_logout(request):
    logout(request)
    return redirect('/')