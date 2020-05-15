from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.forms.profile_info_form import ProfileForm
from user.forms.user_register_form import RegisterCustomerForm
from user.models import profile_info, SearchHistory


def register(request):
    if request.method == "POST":
        form = RegisterCustomerForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user_info = profile_info()
            user_info.user = user
            user_info.save()
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
            s = True
            profile = form.save(commit=False)
            profile.user_id = request.user.id
            profile.save()
        else:
            s= False
        return render(request, "user/profile_info.html", {
            "form": ProfileForm(instance=profile), "success": s
        })

    return render(request, "user/profile_info.html", {
        "form": ProfileForm(instance=profile)
    })


@login_required
def search_history(request):
    s = SearchHistory.objects.filter(user=request.user.id)
    return render(request, "user/search_history.html", {
        "search_history": s
    })