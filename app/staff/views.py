from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from staff.forms.product_form import ProductCreateForm, CategoryCreateForm
from CC.models import Image, Category, Product
from django.contrib.auth.models import User
from staff.forms.staff_register_form import RegisterStaffForm
from user.forms.user_register_form import RegisterCustomerForm


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
        form = AuthenticationForm(request.POST)
        return render(request, "staff/login.html", {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, "staff/login.html", {'form': form})


def dashboard(request):
    return render(request, "staff/dashboard.html")


def products(request):
    product = Product.objects.all()
    return render(request, "staff/products.html", {'products': product})


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


def update_product(request, slug):
    product = Product.objects.get(id=slug)
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
            form = ProductCreateForm(instance=product)
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


def view_staff(request):
    all_users = User.objects.all()
    staff_list = []
    for user in all_users:
        if user.is_superuser or user.is_staff:
            staff_list.append(user)
    return render(request, "staff/view_staff.html", {
        'staff_list': staff_list
    })


def register_staff(request):
    if request.method == "POST":
        form = RegisterStaffForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_staff")
        else:
            return render(request, "staff/register_staff.html", {
                "form": RegisterStaffForm(),
                "form_errors": form.errors
            })
    return render(request, "staff/register_staff.html", {
        "form": RegisterStaffForm()
    })


def update_staff(request, slug):
    staff = User.objects.get(username=slug)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        is_superuser = request.POST.get("is_superuser")
        if first_name != "" and last_name != "":
            staff.first_name = first_name
            staff.last_name = last_name
            if is_superuser == "on":
                staff.is_superuser = True
            else:
                staff.is_superuser = False
            staff.save()
            return render(request, "staff/update_staff.html", {
                "staff": staff,
                "success": "Upplýsingar hafa verið vistaðar"
            })
        else:
            return render(request, "staff/update_staff.html", {
                "staff": staff,
                "error": "Fornafn og eftirnafn verða að vera fylltir inn"
            })
    return render(request, "staff/update_staff.html", {
        "staff": staff
    })


def view_customers(request):
    all_users = User.objects.all()
    customer_list = []
    for user in all_users:
        if not user.is_superuser and not user.is_staff:
            customer_list.append(user)
    return render(request, "staff/view_customers.html", {
        'customer_list': customer_list
    })


def register_customer(request):
    if request.method == "POST":
        form = RegisterCustomerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_customers")
        else:
            return render(request, "staff/register_customer.html", {
                "form": RegisterCustomerForm(),
                "form_errors": form.errors
            })
    return render(request, "staff/register_customer.html", {
        "form": RegisterCustomerForm()
    })


def update_customer(request, slug):
    customer = User.objects.get(username=slug)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST.get("email")
        if first_name != "" and last_name != "" and email != "":
            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = email
            customer.save()
            return render(request, "staff/update_customer.html", {
                "customer": customer,
                "success": "Upplýsingar hafa verið vistaðar"
            })
        else:
            return render(request, "staff/update_customer.html", {
                "customer": customer,
                "error": "Fornafn og eftirnafn verða að vera fylltir inn"
            })
    return render(request, "staff/update_customer.html", {
        "customer": customer
    })