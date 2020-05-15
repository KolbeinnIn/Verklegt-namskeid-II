from django.forms import ModelForm, widgets
from user.models import profile_info


class ProfileForm(ModelForm):
    class Meta:
        model = profile_info
        exclude = ["user"]
        labels = {
            'first_name': 'Fornafn',
            'last_name': 'Eftirnafn',
            'image_path': 'Prófílmynd url',
            'phone_nr': 'Símanúmer',
            'City': 'Borg/bær',
            'zip_code': 'Póstnúmer',
            'address': 'Heimilisfang',
            'country': 'Land',
        }
        widgets = {
            "first_name": widgets.TextInput(attrs={"class": "form-control"}),
            "last_name": widgets.TextInput(attrs={"class": "form-control"}),
            "image_path": widgets.TextInput(attrs={"class": "form-control"}),
            "phone_nr": widgets.TextInput(attrs={"class": "form-control"}),
            "city": widgets.TextInput(attrs={"class": "form-control"}),
            "zip_code": widgets.TextInput(attrs={"class": "form-control"}),
            "address": widgets.TextInput(attrs={"class": "form-control"}),
            "house_no": widgets.TextInput(attrs={"class": "form-control"}),
            "country": widgets.Select(attrs={"class": "form-control"})
        }
