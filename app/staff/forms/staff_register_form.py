from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterStaffForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "is_superuser")

    def save(self, commit=True):
        user = super(RegisterStaffForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.is_staff = True
        if commit:
            user.save()
        return user
