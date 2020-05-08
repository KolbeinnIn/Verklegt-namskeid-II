from django.shortcuts import render, get_object_or_404
from CC.models import Product
# Create your views here.


def index(request, prod_url):
    product = get_object_or_404(Product, url=prod_url)
    prod_dict = {
        "title": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "image": "images/logo.png",  # TODO: have many images
        "description": product.description
    }
    return render(request, "product/index.html", context=prod_dict)



