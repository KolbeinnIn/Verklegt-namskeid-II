from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'(?P<prod_url>.+)/', views.index, name="product-index"),
    url('add-to-cart', views.add_item_to_cart, name="add-to-cart")
]