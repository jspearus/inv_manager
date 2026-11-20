from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.component_list, name="component_list"),
    path("components/add/", views.component_create, name="component_create"),
    path("components/<int:pk>/edit/", views.component_update, name="component_update"),
    path("components/<int:pk>/delete/", views.component_delete, name="component_delete"),
]
