from django.core.validators import MinValueValidator
from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        if self.value:
            return f"{self.name} ({self.value})"
        return self.name
