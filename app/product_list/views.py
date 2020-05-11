from CC.models import Product
from CC.models import Category
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404


def search(request):
    org_query = request.GET.get("leit")
    query = org_query.split(" ")
    all_products = Product.objects.all()
    prod_list = list(all_products.filter(name__icontains=org_query))
    for word in query:
        result = list(all_products.filter(name__icontains=word)) +\
                 list(all_products.filter(description__icontains=word))

        for product in result:
            if product not in prod_list:
                prod_list.append(product)

    return render(request,
                  "product_list/prod_list.html",
                  context={
                      "header": "Leit:",
                      "prod_list": prod_list,
                      "search": True,
                      "query": "'{}'".format(org_query)
                  })


def _get_parent(category, url_string=""):
    if category is None:
        return url_string

    return _get_parent(category.parent, url_string) + "/" + category.URL_keyword


def _does_cat_exist(category):
    try:
        get_object_or_404(Category, URL_keyword=category)
        return True
    except Http404:
        return False


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


def _get_sub_categories(category, all):
    cat_list = list(all.filter(parent=category))
    if not cat_list:
        return []
    temp_list = []
    for sub in cat_list:
        temp_list.append({sub: _get_sub_categories(sub, all)})
    return temp_list

def print_thing(categories, indent=""):
    for cat, subs in categories.items():
        print(indent, cat)
        for sub in subs:
            if sub:
                print_thing(sub, indent+"-")

def category(request, hierarchy):
    categories = request.get_raw_uri().split("/")[4:]
    if categories[-1] == "":
        categories = categories[:-1]

    last_url = categories[-1]
    if _is_product(last_url):
        return redirect("/vara/" + last_url)

    cat = Category.objects.get(URL_keyword=last_url)
    cat1 = Category.objects.get(URL_keyword="leikjatolvur")
    cat2 = Category.objects.get(URL_keyword="leikir")
    cat3 = Category.objects.get(URL_keyword="aukahlutir")

    all = Category.objects.all()
    category_sidebar = {
        cat1: _get_sub_categories(cat1, all),
        cat2: _get_sub_categories(cat2, all),
        cat3: _get_sub_categories(cat3, all)
    }

    if not cat.status:  # if the category is disabled
        return render(request, "sida fannst ekki.html")

    if _is_complete_url(cat, categories):
        header = cat.name
        elder = get_object_or_404(Category, URL_keyword=categories[0])
        return render(request,
                      "product_list/prod_list.html",
                      context={
                          "header": header,
                          "prod_list": list(Product.objects.filter(category=cat)),
                          "elder": elder,  # TODO: elder dæmið
                          "categories": category_sidebar,
                          "parent": ""
                      })
    else:
        if _does_cat_exist(last_url):
            new_url_string = "/flokkur" + _get_parent(cat)
            return redirect(new_url_string)
