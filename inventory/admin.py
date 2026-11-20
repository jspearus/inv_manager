from django.contrib import admin

from .models import Component


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "quantity", "location", "updated_at")
    search_fields = ("name", "value", "description", "location")
    ordering = ("name",)
