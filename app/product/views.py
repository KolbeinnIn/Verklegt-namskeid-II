from django.shortcuts import render, get_object_or_404, redirect
from CC.models import Product
from django import template


def lmao(prod):
    print(prod.name)


def index(request, prod_url):
    return render(request, "product/index.html",
                  context={
                      'product': get_object_or_404(Product, URL_keyword=prod_url),
                      'some_func': lmao
                  })


def add_item_to_cart(request):
    prod_url = request.GET.get("vara")

    return redirect("/vara/" + prod_url)
