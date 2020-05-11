from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_staff_view, name="login_staff"),
    path("logout", LogoutView.as_view(next_page="login_staff"), name="logout_staff"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("create_product", views.create_product, name="create_product"),
    path("create_category", views.create_category, name="create_category"),
    path("products", views.products, name="products"),
    path("update-product/<str:slug>", views.update_product, name="update-product"),
    path("view-staff", views.view_staff, name="view_staff"),
    path("register-staff", views.register_staff, name="register_staff"),
    path("update-staff/<str:slug>", views.update_staff, name="update_staff"),
    path("view-customers", views.view_customers, name="view_customers"),
    path("register-customers", views.register_customer, name="register_customer"),
    path("update-customer/<str:slug>", views.update_customer, name="update_customer"),
]
