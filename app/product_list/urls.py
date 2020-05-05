from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="prod_list-index"),
    path("<int:id>", views.prod_by_id, name="prod-index"),
]
