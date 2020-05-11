from django.shortcuts import render

# Create your views here.
from CC.models import Product
from CC.models import Category
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
# Create your views here.


def search(request):
    return render(request,
                  "product_list/prod_list.html",
                  context={
                      "header": "Search",
                      "prod_list": list(Product.objects.all())
                  })


def _get_parent(category, url_string=""):
    if category is None:
        return url_string

    return _get_parent(category.parent, url_string) + "/" +category.URL_keyword


def _does_cat_exist(category):
    try:
        get_object_or_404(Category, URL_keyword=category)
        return True
    except Http404:
        return False


def _is_parent(parent, child):
    if child is None:
        return False
    if parent == child:
        return True
    child = Category.objects.get(URL_keyword=child).parent.URL_keyword
    return _is_parent(parent, child)


def _is_complete_url(cat, url):
    if not url and cat is None:
        return True
    if not url:
        return False
    if cat is None:
        return False
    if cat.URL_keyword == url[-1]:
        return _is_complete_url(cat.parent, url[:-1])
    return False


def _is_product(slug):
    try:
        get_object_or_404(Product, URL_keyword=slug)
        return True
    except Http404:
        return False


def category(request, hierarchy):
    categories = request.get_raw_uri().split("/")[4:]
    if categories[-1] == "":
        categories = categories[:-1]

    last_url = categories[-1]
    if _is_product(last_url):
        return redirect("/vara/"+last_url)

    cat = Category.objects.get(URL_keyword=last_url)
    if _is_complete_url(cat, categories):
        header = cat.name
        elder = get_object_or_404(Category, URL_keyword=categories[0])
        return render(request,
                      "product_list/prod_list.html",
                      context={
                          "header": header,
                          # "prod_list": list(Category.objects.get(URL_keyword=cat_url).product.all()),
                          "prod_list": list(Product.objects.all()),
                          "elder": elder
                      })
    else:
        if _does_cat_exist(last_url):
            new_url_string = "/flokkur"+_get_parent(cat)
            return redirect(new_url_string)


