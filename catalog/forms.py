from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version


class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'from-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'description')
        exclude = ('created_at', 'updated_at')

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for words in forbidden_words:
            if words in cleaned_data:
                raise forms.ValidationError('Вы ввели запрещенное слово в название товара')
            return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for words in forbidden_words:
            if words in cleaned_data:
                raise forms.ValidationError('Вы ввели запрещенное слово в описание товара')
            return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

        name = forms.CharField(widget=forms.TextInput(attrs={'class': 'my_fields'}))
