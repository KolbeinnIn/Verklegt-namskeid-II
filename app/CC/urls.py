from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="CC-index"),
    path("/<int:id>", views.index, name="CC-index-product")
]