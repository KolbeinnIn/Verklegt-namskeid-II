import json
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from CC.models import Product, Cart, CartItem, Order
from user.models import profile_info, country


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response


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
    product = Product.objects.get(id=prod_id)

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
        try:
            person_info = get_object_or_404(profile_info, user=request.user)
        except Http404:
            person_info = profile_info()
            person_info.user = request.user
            person_info.save()

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
        order = Order.objects.filter(cart_id=cart.id).first()
        if order:
            cart = Cart()
            if person_info:
                cart.person_info = person_info
            else:
                cart.session_id = session_id
            cart.save()

    return cart


def change_quantity(request):
    # Get parameters from request
    cart_item_id = request.POST.get("cart_item_id", None)
    cart_id = request.POST.get("cart_id", None)
    quantity = request.POST.get("quantity", None)

    # Get cartitem from cart
    cart = Cart.objects.get(id=cart_id)
    cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)

    # Change quantity and save in db
    cart_item.quantity = quantity
    cart_item.save()
    return HttpResponse("Quantity changed")


def delete_from_cart(request):
    # Get parameters from request
    cart_item_id = request.POST.get("cart_item_id", None)
    cart_id = request.POST.get("cart_id", None)

    # Get cartitem from cart
    cart = Cart.objects.get(id=cart_id)
    cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)

    # Delete cartitem from db
    cart_item.delete()
    return HttpResponse("Delete successful")


def recieve_updated_cart(request):
    # Get cartitem from cart
    cart = create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    updated_cart = []
    # Get information from all items and put into json format
    for item in cart_items:
        # Get actual product to get the image of product
        actual_product = Product.objects.get(id=item.prod_id)
        image = actual_product.image.first()
        # Create json object and append to updated cart list
        cart_item = {"name": item.prod_name, "quantity": item.quantity, "price": item.unit_price, "image": image.relative_path}
        updated_cart.append(cart_item)
    return JsonResponse(updated_cart, safe=False)


def update_create_person_info(request):
    # Get parameters from request
    request_body = json.loads(request.body)
    person_info_dict = request_body["personal_info"]
    cart_id = int(request_body["cart_id"])
    shipping = request_body["shipping"]
    cart = Cart.objects.get(id=cart_id)
    cart.shipping = shipping

    # Check if user has already a person info associated with his cart
    if cart.person_info:
        person_info = cart.person_info
    # Else we create a new profile info for the user and link it to his cart
    else:
        person_info = profile_info()
        cart.person_info = person_info

    # Set the new parameters of person info to the ones from request
    person_info.first_name = person_info_dict["first_name"]
    person_info.last_name = person_info_dict["last_name"]
    person_info.phone_nr = person_info_dict["phone"]
    person_info.city = person_info_dict["city"]
    person_info.zip_code = person_info_dict["zip"]
    person_info.address = person_info_dict["address"]
    country_obj = country.objects.get(name=person_info_dict["country"])
    person_info.country = country_obj

    # save the new parameters
    person_info.save()
    cart.save()
    return HttpResponse("Update/create successful")


