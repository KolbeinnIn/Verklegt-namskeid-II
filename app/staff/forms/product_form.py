from django.forms import ModelForm, widgets
from django import forms
from CC.models import Product, Category


class ProductCreateForm(ModelForm):
    image = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-9 form-control mt-2 align-self-center', 'id': '0', 'oninput': 'load_img(this)'}))

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
        fields = ['name', 'description', 'price', 'discount', 'manufacturer', 'P_EAN', 'quantity', 'URL_keyword',
                  'status', 'category']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': widgets.TextInput(attrs={'class': 'form-control'}),
            'URL_keyword': widgets.TextInput(attrs={'class': 'form-control'}),
            'P_EAN': widgets.TextInput(attrs={'class': 'form-control'}),
            'quantity': widgets.NumberInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            'discount': widgets.NumberInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'status': widgets.Select(attrs={'class': 'form-control'}, choices=[(True, 'Virkt'), (False, 'Óvirkt')]),
            'category': widgets.SelectMultiple(attrs={'class': 'form-control'})
        }


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['id', 'full_name']
        labels = {
            'name': 'Nafn',
            'status': 'Staða',
            'URL_keyword': 'URL',
            'parent': 'Yfirflokkur'
        }
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'status': widgets.Select(attrs={'class': 'form-control'}, choices=[(True, 'Virkt'), (False, 'Óvirkt')]),
            'URL_keyword': widgets.TextInput(attrs={'class': 'form-control'}),
            'parent': widgets.Select(attrs={'class': 'form-control'})
        }