from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login_staff"),
    path("dashboard", views.create_product, name="dashboard"),
    path("create_product", views.create_product, name="create_product"),
    path("create_category", views.create_category, name="create_category"),
]
