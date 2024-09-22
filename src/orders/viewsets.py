from django.shortcuts import render

from rest_framework.response import Response
from src.abstract.viewsets import AbstractViewSet
from src.orders.models import Orders
from src.orders.serializer import OrderSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

class OrderViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "put",)
    serializer_class=OrderSerializer
    permission_classes=(AllowAny,)
    pagination_class=PageNumberPagination
    search_fields=('cus_name','cus_address','cus_email')
    filterset_fields=['user__public_id',]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Orders.object.all()
        use_pk = self.kwargs.get('use_pk',None)
        if use_pk is None:
            return Orders.object.all()
        queryset = Orders.object.filter(user__public_id=use_pk)
        return queryset
    
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)
    
    def get_object(self):
        obj = Orders.object.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


