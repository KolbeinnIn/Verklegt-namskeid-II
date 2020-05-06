from django.shortcuts import render,redirect
from staff.forms.product_form import ProductCreateForm

# Create your views here.
def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            product = form.save()
            print(product)
            return redirect('staff')

    else:
        form = ProductCreateForm()
    return render(request, "staff/create_product.html", {
        'form': form
    })