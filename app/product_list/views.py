from django.http import Http404
from CC.models import Product, Category
from django.shortcuts import render, get_object_or_404, redirect
from user.models import SearchHistory


def search(request):
    org_query = request.GET.get("leit")
    if org_query is None:
        return redirect("/")
    query = org_query.split(" ")
    all_products = Product.objects.all()
    prod_list = list(all_products.filter(name__icontains=org_query, status=True))
    for word in query:
        result = list(all_products.filter(name__icontains=word, status=True)) + \
                 list(all_products.filter(description__icontains=word, status=True))
        for product in result:
            if product not in prod_list:
                prod_list.append(product)
    if request.user.is_authenticated:
        s = SearchHistory(user=request.user, search_query=org_query)
        s.save()
    all = Category.objects.all()
    category_sidebar = get_category_sidebar(all)

    return render(request,
                  "product_list/prod_list.html",
                  context={
                      "header": "Leit:",
                      "prod_list": prod_list,
                      "search": True,
                      "query": "'{}'".format(org_query),
                      "categories": category_sidebar,
                      "sidebars": True,
                      "filter": "Flokkar"
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
    # gets a category and a list of urls
    # and recursively checks if they are the same
    # cat acts like a singly linked list, a category only knows its parent (node knows next)
    if not url and cat is None:
        return True
    if not url:
        return False
    if cat is None:
        return False
    if cat.URL_keyword == url[-1]:
        return _is_complete_url(cat.parent, url[:-1])
    return False


#_get_sub_categories is a cool function
# because categories sort of act like a singly linked list( a category only knows its parent)
# I have to recursively create a list of dictionaries, which has category as key and lists of dictionaries as values
# [{category_obj: [{sub_category_obj: [{sub_sub_category_obj: []}]}]}]
# It's a neat way of creating the filter sidebar by using the categories as filters
def _get_sub_categories(category, all):
    cat_list = list(all.filter(parent=category))
    if not cat_list:
        return []
    temp_list = []
    for sub in cat_list:
        if sub.status:
            temp_list.append({sub: _get_sub_categories(sub, all)})
    return temp_list


def get_category_sidebar(all):  # used in search, serves categories as a sidebar
    # with each category that has children having a "+" which activates a dropdown
    cat1 = all.get(URL_keyword="leikjatolvur")
    cat2 = all.get(URL_keyword="leikir")
    cat3 = all.get(URL_keyword="aukahlutir")
    return {
        cat1: _get_sub_categories(cat1, all),
        cat2: _get_sub_categories(cat2, all),
        cat3: _get_sub_categories(cat3, all)
    }


def category(request, hierarchy):  # the "hierarchy" parameter needs to be there even though it is not used.
    categories = request.path_info.split("/")[2:]
    if categories[-1] == "":
        categories = categories[:-1]

    last_url = categories[-1]
    all = Category.objects.all()
    try:
        cat = all.get(URL_keyword=last_url)
    except:
        raise Http404

    if not cat.status:  # if the category is disabled
        raise Http404

    if _is_complete_url(cat, categories):
        elder = get_object_or_404(Category, URL_keyword=categories[0])
        elder_subs = {}
        for sub_cat in _get_sub_categories(elder, all):
            for sub_cat_name, children in sub_cat.items():
                elder_subs[sub_cat_name] = children

        header = cat.name
        order_no = request.GET.get("rodun")
        if order_no:
            order = ""
            # this is for getting the order by correct
            # "name" orders by name ascending, "-name" orders by name descending
            if order_no == "1":
                order = "name"
            elif order_no == "2":
                order = "-name"
            elif order_no == "3":
                order = "-total"
            elif order_no == "4":
                order = "total"
            the_list = list(Product.objects.filter(category=cat, status=True).order_by(order))
        else:
            the_list = list(Product.objects.filter(category=cat, status=True).order_by("total"))
        return render(request,
                      "product_list/prod_list.html",
                      context={
                          "header": header,
                          "prod_list": the_list,
                          "categories": elder_subs,
                          "parent": "",
                          "sidebars": True,
                          "filter": "Filter"
                      })
    else:
        if _does_cat_exist(last_url):
            new_url_string = "/flokkur" + _get_parent(cat)
            return redirect(new_url_string)
