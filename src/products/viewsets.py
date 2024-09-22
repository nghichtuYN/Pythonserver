from rest_framework.response import Response
from django.http import Http404
from src.abstract.viewsets import AbstractViewSet
from src.products.models import Products
from src.products.serializers import ProductsSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination


class ProductViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "put", "delete")
    serializer_class = ProductsSerializer
    permission_classes = (AllowAny,)
    pagination_class=PageNumberPagination
    search_fields=('product_name','product_category__category_name','brand__brand_name',)
    filterset_fields=['product_category__public_id',]
    def get_queryset(self):
        return Products.object.all()

    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)


    def get_object(self):
        obj = Products.object.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def delete_many_products(self,request):
        list_product = request.data.get('products', [])
        try:
            Products.object.delete_many(list_product)
            return Response({"detail": "DELETED"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        