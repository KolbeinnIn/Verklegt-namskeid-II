from django.shortcuts import render

# Create your views here.
from CC.models import Product
from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    return render(request, "product_list/prod_list.html", context={"category_name": "Placeholder", "prod_list": list(Product.objects.all())})



def prod_by_id(request, id):
    return render(request, "product_list/prod_details.html", context={"product": get_object_or_404(Product, pk=id)})




