from django.shortcuts import render,redirect
from staff.forms.product_form import ProductCreateForm
from CC.models import Image

# Create your views here.
def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            product = form.save()
            image = Image(relative_path=request.POST['image'], product=product)
            image.save()
            return redirect('')

    else:
        form = ProductCreateForm()
    return render(request, "staff/create_product.html", {
        'form': form
    })