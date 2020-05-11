from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_staff_view, name="login_staff"),
    path("logout", LogoutView.as_view(next_page="login_staff"), name="logout"),
    path("dashboard", views.create_product, name="dashboard"),
    path("create_product", views.create_product, name="create_product"),
    path("create_category", views.create_category, name="create_category"),
    path("products", views.products, name="products"),
    path("update-product/<str:slug>", views.update_product, name="update-product")
]
