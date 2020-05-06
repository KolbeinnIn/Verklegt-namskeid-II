from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.isValid():
            form.save()
            return redirect("login")
    return render(request, "User/register.html", {
        'form': UserCreationForm()
    })