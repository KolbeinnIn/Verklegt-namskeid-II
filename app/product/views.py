from django.shortcuts import render, get_object_or_404, redirect
from CC.models import Product, Cart, CartItem
from user.models import profile_info


def index(request, prod_url):
    return render(request, "product/index.html", context={'product': get_object_or_404(Product, URL_keyword=prod_url)})


def add_item_to_cart(request):
    prod_url = request.GET.get("vara")
    product = Product.objects.filter(URL_keyword=prod_url).first()
    if product:
        # if the user is logged in we will store
        if request.user.is_authenticated:
            person_info = profile_info.objects.filter(user=request.user).first()
            cart = Cart.objects.filter(person_info=person_info).last()
            # If cart exists then add item to the cart else create the cart and add item to it
            if not cart:
                cart = Cart()
                cart.person_info = person_info
                cart.save()
            cart_item = CartItem()
            cart_item.quantity = 1
            cart_item.unit_price = product.total
            cart_item.product = product
            cart_item.cart = cart
            cart_item.save()
            print(cart_item)
            print(CartItem.objects.all().first())
        else:
            # add to cookies
            a = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ég er að brjálast"
            print(a)
        return redirect("/vara/" + prod_url)
    else:
        return redirect('CC-index')