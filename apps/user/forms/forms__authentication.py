from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _
from apps.user.models import CustomUser



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'data-error': 'Введите Email корректно',
        'placeholder' : 'Введите Email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder' : 'Пароль'
    }))

    error_messages = {
        'user_not_exists' : _("Пользователь с E-mail '%(username)s' не зарегестрирован в ситсеме"),
        'invalid_login': _("Пароль введен не верно"),
        'inactive': _("This account is inactive."),
    }

    class Meta:
        model = CustomUser
        fields = ['username','password']


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.label=""
            field.widget.attrs['id'] = f'login_form_{name}'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = CustomUser.objects.get(email=username)
            except:
                user = None
                raise forms.ValidationError(
                    self.error_messages['user_not_exists'],
                    code='user_not_exists',
                    params={'username': username},
                )
            if user:
                self.user_cache = authenticate(username=username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
                else:
                    self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

       
class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(widget=forms.TextInput(attrs={
    #     'data-error' :  'Введите Email корректно',
    #     'placeholder' : 'Введите Email',
    # }))
 
    class Meta:
        model = CustomUser
        fields = ['name','email', 'password1', 'password2']
     
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'registration_form_{name}'
            field.label=""

        self.fields['password1'].widget.attrs['data-error']  = 'Пароль имеет не верный формат'
        self.fields['password1'].widget.attrs['placeholder'] = 'Придумайте пароль'
        self.fields['password2'].widget.attrs['data-error']  = 'Пароли не совпадают'
        self.fields['password2'].widget.attrs['placeholder'] = 'Введите пароль еще раз'

