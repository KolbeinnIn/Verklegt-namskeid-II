from django.conf.urls import url
from django.urls import path

from . import views
urlpatterns = [
    path('<prod_url>', views.index, name="product-index"),
    url('add-to-cart', views.add_item_to_cart, name="add-to-cart")
]