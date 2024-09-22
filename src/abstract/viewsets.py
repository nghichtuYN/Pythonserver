from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend



class AbstractViewSet(viewsets.ModelViewSet):
    ordering_fields = ["updated", "created"]
    ordering = ["-updated"]
    filter_backends=(SearchFilter,DjangoFilterBackend)
