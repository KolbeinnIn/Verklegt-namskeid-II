from django import forms
from django.forms import widgets
from user.forms.profile_info_form import ProfileForm
from user.models import profile_info


class PersonalInfoForm(ProfileForm):
    class Meta:
        model = profile_info
        exclude = ["user", "image_path"]
        widgets = {
            "first_name": widgets.TextInput(attrs={"class": "form-control", 'required': True}),
            "last_name": widgets.TextInput(attrs={"class": "form-control"}),
            "phone_nr": widgets.TextInput(attrs={"class": "form-control"}),
            "city": widgets.TextInput(attrs={"class": "form-control"}),
            "zip_code": widgets.TextInput(attrs={"class": "form-control"}),
            "address": widgets.TextInput(attrs={"class": "form-control"}),
            "country": widgets.Select(attrs={"class": "form-control"})
        }


class PaymentInfoForm(forms.Form):
    cardholder_name = forms.CharField(label="Cardholder name", widget=forms.TextInput(attrs={"class": "form-control"}))
    card_number = forms.CharField(label="Card number", widget=forms.TextInput(attrs={"class": "form-control", "value":""}))
    expiration_date = forms.CharField(label="Exipration date", widget=forms.TextInput(attrs={"class": "form-control"}))
    cvc = forms.CharField(label="CVC", widget=forms.TextInput(attrs={"class": "form-control"}))
