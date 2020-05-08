from django.shortcuts import render
from CC.models import Product


def index(request):
    popular_product_list = []
    new_product_list = []
    if len(Product.objects.all()) > 6:
        popular_product_list = Product.objects.all()[:6]
    if len(Product.objects.all()) > 10:
        new_product_list = Product.objects.all()[len(Product.objects.all()) - 6:]

    return render(request,
                  "CC/index.html",
                  context={
                      "popular_product_list": popular_product_list,
                      "new_product_list": new_product_list
                  })
