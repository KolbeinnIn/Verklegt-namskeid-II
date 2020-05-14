from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="CC-index"),
    path('add-to-cart', views.add_item_to_cart, name="add-to-cart"),
    path('change-quantity', views.change_quantity, name="change-quantity"),
    path('delete-from-cart', views.delete_from_cart, name="delete-from-cart"),
    path('recieve-updated-cart', views.recieve_updated_cart, name="lala"),
    path('update-create-person-info', views.update_create_person_info, name="update-create-person-info")
]