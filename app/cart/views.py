from django.http import Http404
from django.shortcuts import render, get_object_or_404
from CC.models import CartItem, Product, Order
from CC.views import create_cart
from cart.forms.cart_forms import PersonalInfoForm, PaymentInfoForm
from user.models import profile_info


def index(request):
    personal_info = profile_info.objects.filter(user=request.user.id).first()
    personal_info_form = PersonalInfoForm(instance=personal_info)

    cart = create_cart(request)
    products = list(CartItem.objects.filter(cart=cart))
    prod_dict = {}
    total = 0
    for item in products:
        # Try except ef varan er ekki til þá eyða henni úr cart items
        try:
            actual_product = get_object_or_404(Product, pk=item.prod_id)
            image = actual_product.image.first()
            prod_dict[item] = image.relative_path
            total += (item.unit_price * item.quantity)
        except Http404:
            item.delete()

    return render(request, "cart/index.html",
                  context={
                      "products": prod_dict,
                      "personal_info_form": personal_info_form,
                      "payment_info_form": PaymentInfoForm,
                      "total": total,
                      "cart_id": cart.id,
                  })


def success(request):
    # Get parameters from request
    cart = create_cart(request)
    cart_items = list(CartItem.objects.filter(cart=cart))

    # Check if there are any products in the cart
    if cart_items:
        # Get the total amount for products in cart
        total = 0
        for item in cart_items:
            total += (item.unit_price * item.quantity)

        # Create order with given parameters
        order = Order()
        order.cart = cart
        order.total = total
        order.save()
    return render(request, "cart/success.html")
