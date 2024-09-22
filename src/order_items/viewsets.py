from rest_framework.response import Response
from django.http import Http404
from src.abstract.viewsets import AbstractViewSet
from src.order_items.models import OrderItems
from src.order_items.serializers import OrderItemsSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny


class OrderItemsViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "put", "delete")
    serializer_class = OrderItemsSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return OrderItems.object.all()
        orders_pk = self.kwargs['orders_pk']
        if orders_pk is None:
            return Http404
        queryset = OrderItems.object.filter(orders__public_id=orders_pk)
        return queryset
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)
    
    
    def get_object(self):
        obj = OrderItems.object.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)