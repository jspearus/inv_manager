from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from inventory.api import ComponentViewSet

router = DefaultRouter()
router.register("components", ComponentViewSet, basename="component")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("", include("inventory.urls")),
]
