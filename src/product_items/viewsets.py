from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from ..abstract.viewsets import AbstractViewSet
from .models import ProductItems
from .serializers import ProductItemsSerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from src.products.models import Products

class ProductItemsViewSet(AbstractViewSet):
    http_method_names = ("put", "post", "get", "delete")
    permission_classes = (AllowAny,)
    serializer_class = ProductItemsSerializer
    pagination_class=PageNumberPagination
    search_fields=('product__product_name','colour__colour_name','product__product_name')
    filterset_fields=['original_price','product__public_id',]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductItems.object.all()
        product_pk = self.kwargs.get('product_pk',None)
        if product_pk is None:
            return ProductItems.object.all()
        queryset = ProductItems.object.filter(product__public_id=product_pk)
        return queryset
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

    def get_object(self):
        obj = ProductItems.object.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False,methods=['post'])
    def delete_many_product_items(self,request):
        productItems = request.data.get('productItems', [])
        try:
            ProductItems.object.delete_many(productItems)
            return Response({"detail": "DELETED"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)