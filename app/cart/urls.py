from django.urls import path
from django.conf.urls import url

from . import views
urlpatterns = [
    url('success/', views.success, name="cart-success"),
    url('', views.index, name="cart-index"),
]
