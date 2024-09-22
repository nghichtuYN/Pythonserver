from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import AllowAny
from ..abstract.viewsets import AbstractViewSet
from .serializers import ColourSerializer
from .models import Colour
from rest_framework import status
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404


class ColourViewSet(AbstractViewSet):
    http_method_names = ("post", "put", "get", "delete")
    permission_classes = (AllowAny,)
    serializer_class = ColourSerializer
    
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Colour.object.all()
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(Colour, public_id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    