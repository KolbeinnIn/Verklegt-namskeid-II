from django.shortcuts import render
from cart.forms.cart_forms import PersonalInfoForm, PaymentInfoForm
from user.models import profile_info


def index(request):
    personal_info = profile_info.objects.filter(user=request.user.id).first()
    personal_info_form = PersonalInfoForm(instance=personal_info)
    return render(request, "cart/index.html", context={'name': "The big boy with long name", "amount": 1,"price": 22000, "total": 22000, "personal_info_form": personal_info_form, "payment_info_form": PaymentInfoForm})
