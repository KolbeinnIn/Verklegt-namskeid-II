from django.shortcuts import render, redirect
from CC.models import Product, Cart, CartItem, Shipping, Category, Order
from user.models import profile_info

def index(request):
    popular_product_list = []
    new_product_list = []
    all = list(Product.objects.all())
    if len(all) > 6:
        popular_product_list = all[:6]
    if len(all) > 10:
        new_product_list = all[len(all) - 6:]

    return render(request,
                  "CC/index.html",
                  context={
                      "popular_product_list": popular_product_list,
                      "new_product_list": new_product_list
                  })


def add_item_to_cart(request):
    # Get parameters from request
    prod_url = request.GET.get("prod")
    quantity = request.GET.get("quantity")
    # Get product from parameters
    product = Product.objects.filter(URL_keyword=prod_url).first()
    if product:
        # if the user is logged in we will store the cart in the database
        if request.user.is_authenticated:
            person_info = profile_info.objects.filter(user=request.user).first()
            cart = Cart.objects.filter(person_info=person_info).last()

            # If cart doesnt exists we need to create it
            if not cart:
                cart = Cart()
                cart.person_info = person_info
                cart.save()
            else:
                order = Order.objects.filter(cart=cart).first()
                # Check if cart been made into order, then we need to assign new one
                if order:
                    cart = Cart()
                    cart.person_info = person_info
                    cart.save()

            cart_item = CartItem.objects.filter(product=product, cart=cart).first()
            # If the item is not already in this cart we need to create it
            if not cart_item:
                cart_item = CartItem()
                cart_item.product = product
                cart_item.cart = cart
            # Update parameters of cart item and save it
            cart_item.quantity += int(quantity)
            cart_item.unit_price = product.total
            cart_item.save()
        else:
            # add to cookies
            a = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ég er að brjálast"
        return redirect("/vara/" + prod_url)
    else:
        # Item dosnt exist so we send them to the front page
        return redirect('CC-index')