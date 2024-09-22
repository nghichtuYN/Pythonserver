from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from src.abstract.viewsets import AbstractViewSet
from src.size_category.serializers import SizeCategorySerializer
from src.size_category.models import SizeCategory
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action


class SizeCategoryViewSet(AbstractViewSet):
    http_method_names = ("post", "put", "get", "delete")
    permission_classes = (AllowAny,)
    serializer_class = SizeCategorySerializer
    pagination_class=PageNumberPagination
    search_fields=('category_name',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return SizeCategory.objects.all()

    def get_object(self):
        obj = SizeCategory.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=False, methods=['get'])
    def no_pagination(self, request):
        queryset = SizeCategory.object.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def delete_many_size_categories(self,request):
        size_categories = request.data.get('size_categories', [])
        try:
            SizeCategory.objects.delete_many(size_categories)
            return Response({"detail": "DELETED"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)
