from django.urls import path
from . import views

urlpatterns = [
    path("leit", views.search, name="leit"),
    path("<str:cat_url>", views.category, name="category"),
]
