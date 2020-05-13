from django.shortcuts import render, get_object_or_404
from CC.models import Product


def index(request, prod_url):
    return render(request, "product/index.html", context={'product': get_object_or_404(Product, URL_keyword=prod_url)})