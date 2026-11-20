from rest_framework import filters, viewsets

from .models import Component
from .serializers import ComponentSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "value", "description", "location")
