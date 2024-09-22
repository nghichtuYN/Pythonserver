from rest_framework.response import Response
from rest_framework import status
from ..abstract.viewsets import AbstractViewSet
from .models import Brand
from .serializers import BrandSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action


class BrandViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "put", "delete")
    permission_classes = (AllowAny,)
    serializer_class = BrandSerializer

    def get_queryset(self):
        return Brand.object.all()

    def get_object(self):
        obj = Brand.object.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def no_pagination(self, request):
        queryset = Brand.object.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
