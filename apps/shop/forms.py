from django import forms
from .models import Messages



class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = '__all__'
        exclude = ['create']

    def __init__(self, *args, **kwargs):
        super(MessagesForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'conatct_form_{name}'
            field.label=""

        