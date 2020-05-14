from django.shortcuts import render, redirect
from CC.models import Product, Cart, CartItem, Order
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
    prod_id = request.GET.get("prod")
    quantity = request.GET.get("quantity")

    # Get product from parameters
    product = Product.objects.filter(id=prod_id).first()

    if product:
        cart = create_cart(request)
        cart_item = CartItem.objects.filter(prod_id=product.id, cart=cart).first()

        # If the item is not already in this cart we need to create it
        if not cart_item:
            cart_item = CartItem()
            cart_item.prod_id = int(product.id)
            cart_item.quantity = quantity
            cart_item.cart = cart
        else:
            cart_item.quantity += int(quantity)

        # Update parameters of cart item and save it
        cart_item.prod_name = product.name
        cart_item.unit_price = product.total
        cart_item.save()
        request.session['cart_quantity'] += int(quantity)
        return redirect("/vara/" + product.URL_keyword)
    else:
        # Item dosnt exist so we send them to the front page
        return redirect('CC-index')


def create_cart(request):
    # if the user is logged in we will store the cart with the user
    person_info = None
    # if user is not logged in we need to store the cart with the session id/key
    session_id = None

    if request.user.is_authenticated:
        # get the person info of user and cart associated with it
        person_info = profile_info.objects.filter(user=request.user).first()
        cart = Cart.objects.filter(person_info=person_info).last()
    else:
        # if user is not in and there is not a session we must create one
        if not request.session.exists(request.session.session_key):
            request.session.create()
        # get the session_id and cart associated with it
        session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).last()

    # If cart that we tried to get doesn't exists we need to create it
    if not cart:
        cart = Cart()
        if person_info:
            cart.person_info = person_info
        else:
            cart.session_id = session_id
        cart.save()
    # Check if cart been made into order, then we need to assign new one
    else:
        order = Order.objects.filter(cart=cart).first()
        if order:
            cart = Cart()
            if person_info:
                cart.person_info = person_info
            else:
                cart.session_id = session_id
            cart.save()

    return cart


def change_quantity(request):
    cartItem_id = request.POST.get("cart_item_id", None)
    cart_id = request.POST.get("cart_id", None)
    quantity = request.POST.get("quantity", None)
    print(cartItem_id)
    return


def delete_from_cart(request):
    return
