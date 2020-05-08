from django.shortcuts import render, redirect
from staff.forms.product_form import ProductCreateForm, CategoryCreateForm
from CC.models import Image, Category

# Create your views here.
def create_product(request):
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
    return render(request, "staff/create_product.html", {
        'form': form
    })


def create_category(request):
    if request.method == 'POST':
        form = CategoryCreateForm(data=request.POST)
        if form.is_valid():
            category = form.save()
            category.check_url()
            return redirect('/')
    else:
        form = CategoryCreateForm()
    return render(request, "staff/create_category.html", {
        'form': form
    })