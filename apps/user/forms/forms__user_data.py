from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import modelformset_factory
from django.forms import BaseFormSet
from django.forms.widgets import DateInput
from django.forms.models import BaseInlineFormSet
from apps.user.models import CustomUser, UserAdress, UserAdressChosen, UserNP, UserNPChosen, UserCompany, UserSubscripton
from apps.catalogue.models import Category
from django.forms.models import inlineformset_factory

class UserDataMainForm(forms.ModelForm):
    birthday = forms.DateField(required=False, widget=DateInput(attrs={
        'type' : 'date', 'format' : '%Y-%d-%m', 'required' : False
    }))

    class Meta:
        model = CustomUser
        fields = [
            'name','surname','patronymic','gender','birthday','language'
        ]

    def __init__(self, *args, **kwargs):
        super(UserDataMainForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        for name, field in self.fields.items():
            field.widget.attrs['id'] = f'user_data_main_{name}'
            field.widget.attrs['data-value'] = ''
            
            if getattr(instance, name) in [None,'']:
                field.widget.attrs['placeholder'] = '-'



class UserDataConstactsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'phone','email'
        ]

    def __init__(self, *args, **kwargs):
        super(UserDataConstactsForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        for name, field in self.fields.items():
            field.widget.attrs['id'] = f'user_data_contacts_{name}'
            field.widget.attrs['data-value'] = ''
            if getattr(instance, name) in [None,'']:
                field.widget.attrs['placeholder'] = '-'





# class UserAdressChosenForm(forms.ModelForm):
#     class Meta:
#         model = UserAdressChosen
#         fields = [
#             'adress'
#         ]

#     def __init__(self, *args, **kwargs):
#         super(UserAdressChosenForm, self).__init__(*args, **kwargs)
#         instance = kwargs['instance']

#         self.fields['adress'].label = 'Приоритетный адрес'
#         self.fields['adress'].queryset =  self.fields['adress'].queryset.filter(parent = kwargs['instance'])
#         self.fields['adress'].initial = instance.adress_chosen.adress.pk
        
#         for name, field in self.fields.items():
#             field.widget.attrs['id'] = f'user_adress_chosen_{name}'
#             field.widget.attrs['data-value'] = ''


    # def save(self, commit=True):
    #     instance = super(UserAdressChosenForm, self).save(commit=False)
    #     UserAdressChosen.objects.filter(parent=instance).update(adress=self.cleaned_data['adress'])
    #     if commit:
    #         instance.save()
    #     return instance
    

# ADRESS CHOSEN
class UserAdressChosenFormSet(BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs

class UserAdressChosenForm(forms.ModelForm):
    class Meta:
        model = UserAdressChosen
        fields = [
            'adress'
        ]

    def __init__(self, parent_object, *args, **kwargs):
        super(UserAdressChosenForm, self).__init__(*args, **kwargs)
       
        self.fields['adress'].label = 'Приоритетный адрес'
        self.fields['adress'].queryset =  self.fields['adress'].queryset.filter(parent=parent_object)
        print(self.fields['adress'].initial)
        # self.fields['adress'].initial = instance.adress_chosen.adress.pk
        
        # for name, field in self.fields.items():
        #     field.widget.attrs['id'] = f'user_adress_chosen_{name}'
        #     field.widget.attrs['data-value'] = ''
       

UserAdressChosenFormSetFactory = inlineformset_factory(
    CustomUser, UserAdressChosen, extra=1,
    fields = [
        'adress'
    ],
    formset = UserAdressChosenFormSet,
    form = UserAdressChosenForm
)



# ADRESS FORM
class UserAdressForm(forms.ModelForm):
    class Meta:
        model = UserAdress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserAdressForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label

UserAdressFromSet = inlineformset_factory(
    CustomUser, UserAdress, extra=1,
    fields = [
        'id','city','street','house','appartment'
    ],
    form = UserAdressForm
)



# COMPANY FORM
class UserCompanyForm(forms.ModelForm):
    class Meta:
        model = UserCompany
        fields = [
            'name','code','email','iban','director','adress'
        ]

    def __init__(self, *args, **kwargs):
        super(UserCompanyForm, self).__init__(*args, **kwargs)
       

UserCompanyFormSet = inlineformset_factory(
    CustomUser, UserCompany, extra=1,
    fields = [
        'name','code','email','iban','director','adress'
    ],
)




class UserSubscriptionForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(parent=None),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = UserSubscripton
        fields = ['category']

    def __init__(self, *args, **kwargs):
        super(UserSubscriptionForm, self).__init__(*args, **kwargs)

       
UserSubscriptionFormSet = inlineformset_factory(
    CustomUser, UserSubscripton, extra=1,
    fields = ['category'],
    form = UserSubscriptionForm
)


