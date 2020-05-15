from CC.models import CartItem, Order
from CC.views import create_cart


def cart_middleware(get_response):
    # Calculates quantity within the cart and displays everywhere on the site
    def middleware(request):
        calculate_cart_quantity(request)
        response = get_response(request)
        return response
    return middleware


def calculate_cart_quantity(request):
    cart = create_cart(request)

    # Check if the cart has been made into an order
    order = Order.objects.filter(cart_id=cart.id).first()
    if not order:
        cart_item_list = list(CartItem.objects.filter(cart=cart))

        # Calculate quantity and set for session
        quantity = 0
        for cart_item in cart_item_list:
            quantity += int(cart_item.quantity)

        request.session['cart_quantity'] = quantity
    # Reset the quantity
    else:
        request.session['cart_quantity'] = 0
