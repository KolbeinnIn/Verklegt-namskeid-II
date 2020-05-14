from django.urls import path
from . import views

urlpatterns = [
    path('<prod_url>', views.index, name="product-index"),
]