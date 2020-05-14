from CC.models import Cart, CartItem, Order
from user.models import profile_info


def cart_middleware(get_response):
    def middleware(request):
        # Code to be executed for each request before the view (and later middleware) are called.
        calculate_cart_quantity(request)
        response = get_response(request)
        # Code to be executed for each request/response after the view is called.
        return response
    return middleware


def calculate_cart_quantity(request):
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

    cart_item_list = list(CartItem.objects.filter(cart=cart))

    quantity = 0
    for cart_item in cart_item_list:
        quantity += int(cart_item.quantity)

    request.session['cart_quantity'] = quantity
