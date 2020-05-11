from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.forms.profile_info_form import ProfileForm
from user.forms.user_register_form import RegisterCustomerForm
from user.models import profile_info


def register(request):
    if request.method == "POST":
        form = RegisterCustomerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, "user/register.html", {
                "form": RegisterCustomerForm(),
                "form_errors": form.errors
            })
    return render(request, "user/register.html", {
        "form": RegisterCustomerForm()
    })


@login_required
def profile(request):
    return render(request, "user/profile.html", context={"profile": profile_info.objects.filter(user=request.user.id).first()})


@login_required
def info(request):
    profile = profile_info.objects.filter(user=request.user.id).first()
    if request.method == "POST":
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = request.user.id
            profile.save()
            return redirect("profile")
    return render(request, "user/profile_info.html", {
        "form": ProfileForm(instance=profile)
    })
