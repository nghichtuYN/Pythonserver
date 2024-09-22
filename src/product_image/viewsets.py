from django.http import Http404
from rest_framework import status
from ..abstract.viewsets import AbstractViewSet
from .serializers import ProductImageSerializer
from .models import ProductImage
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser

class ProductImageViewSet(AbstractViewSet):
    http_method_names = ("post", "put", "get", "delete")
    serializer_class = ProductImageSerializer
    permission_classes = (AllowAny,)
    parser_classes=[MultiPartParser,FormParser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductImage.object.all()
        product_items_pk = self.kwargs['product_item_pk']
        if product_items_pk is None:
            return Http404
        queryset = ProductImage.object.filter(product_items__public_id=product_items_pk)
        return queryset

    def get_object(self):
        obj = ProductImage.object.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    
    
