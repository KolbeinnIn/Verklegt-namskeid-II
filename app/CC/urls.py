from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="CC-index"),
    path('add-to-cart', views.add_item_to_cart, name="add-to-cart"),
]