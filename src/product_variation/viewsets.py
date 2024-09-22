from ..abstract.viewsets import AbstractViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import ProductVariation
from .serializers import ProductVariationSerializer
from django.http import Http404
from rest_framework.decorators import action


class ProductVariationViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "put", "delete")
    permission_classes = (AllowAny,)
    serializer_class = ProductVariationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductVariation.object.all()
        product_items_pk = self.kwargs['product_item_pk']
        if product_items_pk is None:
            return Http404
        queryset = ProductVariation.object.filter(product_items__public_id=product_items_pk).all()
        return queryset

    def get_object(self):
        obj = ProductVariation.object.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def no_pagination(self, request,product_item_pk=None):
        product_item_pk = self.kwargs.get('product_item_pk')
        if not product_item_pk:
            return Response({"detail": "Product item ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        product_variation = ProductVariation.object.filter(product_items__public_id=product_item_pk)
        if not product_variation.exists():
            return Response({"detail": "No ProductItems found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(product_variation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
