from django.urls import path
from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'(?P<prod_url>.+)/', views.index, name="product-index"),
]