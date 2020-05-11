from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StaffLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['Notendanafn eða lykilorð er rangt. Vinsamlegast reyndu aftur.'],)
        if not user.is_staff or not user.admin:
            raise forms.ValidationError(self.error_messages['Notendanafn eða lykilorð er rangt. Vinsamlegast reyndu aftur.'],)
