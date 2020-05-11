from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from staff.forms.product_form import ProductCreateForm, CategoryCreateForm
from CC.models import Image, Category


def login_staff_view(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect("dashboard")
            else:
                form = AuthenticationForm(request.POST)
                return render(request, "staff/login.html", {'form': form})
        else:
            form = AuthenticationForm(request.POST)
            return render(request, "staff/login.html", {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, "staff/login.html", {'form': form})


def dashboard(request):
    return render(request, "staff/dashboard.html")


def create_product(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = ProductCreateForm(data=request.POST)
            if form.is_valid():
                product = form.save()
                product.check_url()
                image = Image(name="Placeholder", relative_path=request.POST['image'])
                image.save()
                product.image.add(image)
                return redirect('/')
        else:
            form = ProductCreateForm()
        return render(request, "staff/create_product.html", {'form': form})
    else:
        return redirect("login_staff")


def create_category(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = CategoryCreateForm(data=request.POST)
            if form.is_valid():
                category = form.save()
                category.initialize()
                return redirect('/')
        else:
            form = CategoryCreateForm()
        return render(request, "staff/create_category.html", {
            'form': form
        })
    else:
        return redirect("login_staff")
