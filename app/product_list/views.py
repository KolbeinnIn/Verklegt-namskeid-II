from django.shortcuts import render

# Create your views here.
from CC.models import Product
from CC.models import Category
from django.shortcuts import render, get_object_or_404

# Create your views here.


def search(request):
    return render(request,
                  "product_list/prod_list.html",
                  context={
                      "header": "Search",
                      "prod_list": list(Product.objects.all())
                  })


def category(request, cat_url):
    result_obj = get_object_or_404(Category, URL_keyword=cat_url)
    header = result_obj.name
    return render(request,
                  "product_list/prod_list.html",
                  context={
                      "header": header,
                      "prod_list": list(Product.objects.all())
                  })




