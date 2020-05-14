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
    product = Product.objects.all().order_by("name")
    return render(request, "staff/view_all_products.html", {'products': product})

# HELPER CLASS MOVE LATER
def create_images_product(images, product):
    for img in images:
        if img != '':
            image = Image(name='Placeholder', relative_path=img)
            image.save()
            product.image.add(image)


def create_product(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = ProductCreateForm(data=request.POST)
            if form.is_valid():
                product = form.save()
                product.initialize()
                images = dict(request.POST)['image']
                create_images_product(images, product)
                product.save()
                return redirect("view_all_products")
        else:
            form = ProductCreateForm()
        return render(request, "staff/create_product.html", {'form': form, 'Title': 'Búa til vöru',
                                                             'path': 'create_product', 'slug': ''})
    else:
        return redirect("login_staff")


def update_product(request, slug):
    if request.user.is_staff or request.user.is_superuser:
        product = Product.objects.get(id=slug)
        if request.method == 'POST':
            form = ProductCreateForm(data=request.POST)
            if form.is_valid():
                print(form)
                product = form.save(commit=False)
                product.id = slug
                images = dict(request.POST)['image']
                old_images = product.image.all()
                for img in old_images:
                    img.delete()
                product.save()
                create_images_product(images, product)
                product.initialize()
                return redirect("view_all_products")
        else:
            form = ProductCreateForm(instance=product)
        return render(request, "staff/create_product.html", {'form': form, 'Title': 'Breyta upplýsingum',
                                                             'images': product.image.all(), 'path': 'update_product',
                                                             'slug': slug})
    else:
        return redirect("login_staff")


def delete_product(request, slug):
    product = Product.objects.get(id=slug)
    images = product.image.all()
    for img in images:
        img.delete()
    product.delete()
    return redirect("view_all_products")


def categories(request):
    category = Category.objects.all().order_by("full_name")
    return render(request, "staff/view_all_categories.html", {'category': category})


def create_category(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = CategoryCreateForm(data=request.POST)
            if form.is_valid():
                category = form.save()
                category.initialize()
                return redirect('view_all_categories')
        else:
            form = CategoryCreateForm()
        return render(request, "staff/create_category.html", {'form': form, 'path': 'create_category',
                                                              'Title': 'Búa til flokk'})
    else:
        return redirect("login_staff")


def update_category(request, slug):
    if request.user.is_staff or request.user.is_superuser:
        category = Category.objects.get(id=slug)
        if request.method == 'POST':
            form = CategoryCreateForm(data=request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.id = slug
                category.initialize()
                return redirect('view_all_categories')
        else:
            form = CategoryCreateForm(instance=category)
        return render(request, "staff/create_category.html", {'form': form, 'slug': slug, 'path': 'update_category',
                                                              'Title': 'Uppfæra flokk'})
    else:
        return redirect("login_staff")


def view_staff(request):
    all_users = User.objects.all()
    staff_list = []
    for user in all_users:
        if user.is_superuser or user.is_staff:
            staff_list.append(user)
    return render(request, "staff/view_all_staff.html", {
        'staff_list': staff_list
    })


def register_staff(request):
    if request.method == "POST":
        form = RegisterStaffForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_all_staff")
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
    return render(request, "staff/view_all_customers.html", {
        'customer_list': customer_list
    })


def register_customer(request):
    if request.method == "POST":
        form = RegisterCustomerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_all_customers")
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