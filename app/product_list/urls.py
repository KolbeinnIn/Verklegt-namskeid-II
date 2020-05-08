from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("leit", views.search, name="leit"),
    url(r'(?P<hierarchy>.+)/', views.category, name="category"),
]

