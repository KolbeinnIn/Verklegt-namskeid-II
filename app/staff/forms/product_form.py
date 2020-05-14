from django.forms import ModelForm, widgets
from django import forms
from CC.models import Product, Category


class ProductCreateForm(ModelForm):
    #image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'img'}))
    class Meta:
        model = Product
        exclude = ['id', 'image', 'total']
        labels = {
            'name': 'Nafn',
            'manufacturer': 'Framleiðandi',
            'URL_keyword': 'URL',
            'P_EAN': 'Strikamerki',
            'quantity': 'Magn',
            'price': 'Verð',
            'discount': 'Afsláttur',
            'description': 'Lýsing',
            'status': 'Staða',
            'category': 'Flokkar',
        }
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': widgets.TextInput(attrs={'class': 'form-control'}),
            'URL_keyword': widgets.TextInput(attrs={'class': 'form-control'}),
            'P_EAN': widgets.TextInput(attrs={'class': 'form-control'}),
            'quantity': widgets.NumberInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            'discount': widgets.NumberInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'status': widgets.Select(attrs={'class': 'form-control'}, choices=[(True, 'Enabled'), (False, 'Disabled')]),
            'category': widgets.SelectMultiple(attrs={'class': 'form-control'})
        }


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['id', 'full_name']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'status': widgets.Select(attrs={'class': 'form-control'}, choices=[(True, 'Enabled'), (False, 'Disabled')]),
            'URL_keyword': widgets.TextInput(attrs={'class': 'form-control'}),
            'parent': widgets.Select(attrs={'class': 'form-control'})
        }