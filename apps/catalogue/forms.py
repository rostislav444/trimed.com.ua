from django import forms
from apps.catalogue_filters.models import Attribute

class CategoryAttributeForm(forms.ModelForm):
    model = 'catalogue_filters.CategoryAttribute'

    class Meta:
        fields = '__all__'

    def __init__(self, parent_object=None, *args, **kwargs):
        super(CategoryAttributeForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs.keys():
            category_attribute = kwargs['instance']
            self.fields['attribute'].queryset = self.fields['attribute'].queryset.filter(pk=category_attribute.attribute.pk)
        else:
            category = parent_object
            if category:
                categories = category.get_ancestors(include_self=True)
                attributes = Attribute.objects.exclude(category__parent__in=categories)
                self.fields['attribute'].queryset = attributes


class CategoryAttributeFormSet(forms.BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs
