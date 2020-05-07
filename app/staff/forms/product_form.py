from django.forms import ModelForm, widgets
from django import forms
from CC.models import Product


class ProductCreateForm(ModelForm):
    image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Product
        exclude = ['id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': widgets.TextInput(attrs={'class': 'form-control'}),
            'url': widgets.TextInput(attrs={'class': 'form-control'}),
            'P_EAN': widgets.TextInput(attrs={'class': 'form-control'}),
            'quantity': widgets.NumberInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            'discount': widgets.NumberInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'status': widgets.CheckboxInput(attrs={'class': 'checkbox'}),
            'category': widgets.Select(attrs={'class': 'form-control'}),
        }