from django.forms import ModelForm, widgets
from user.models import profile_info


class ProfileForm(ModelForm):
    class Meta:
        model = profile_info
        exclude = ["user"]
        widgets = {
            "image_path": widgets.TextInput(attrs={"class": "form-control"}),
            "phone_nr": widgets.TextInput(attrs={"class": "form-control"}),
            "city": widgets.TextInput(attrs={"class": "form-control"}),
            "zip_code": widgets.TextInput(attrs={"class": "form-control"}),
            "street_name": widgets.TextInput(attrs={"class": "form-control"}),
            "house_no": widgets.TextInput(attrs={"class": "form-control"}),
            "country": widgets.Select(attrs={"class": "form-control"})
        }
