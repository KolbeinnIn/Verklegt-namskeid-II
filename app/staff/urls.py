from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path("", LoginView.as_view(template_name="staff/login.html"), name="login_staff"),
    path("create_product", views.create_product, name="create_product"),
    path("create_category", views.create_category, name="create_category"),
]
