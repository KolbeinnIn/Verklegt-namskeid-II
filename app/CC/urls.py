from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="CC-index"),
    path('add-to-cart', views.add_item_to_cart, name="add-to-cart"),
    path('change-quantity', views.change_quantity, name="change-quantity"),
    path('delete-from-cart', views.delete_from_cart, name="delete-from-cart"),
]