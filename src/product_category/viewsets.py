from rest_framework.response import Response
from rest_framework import status
from ..abstract.viewsets import AbstractViewSet
from .models import ProductCategory
from .serializers import ProductCategorySerializer, ChildProductCategorySerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

class ProductCategoryViewSet(AbstractViewSet):
    http_method_names = ("post", "put", "get", "delete")
    serializer_class = ProductCategorySerializer
    permission_classes = (AllowAny,)
    pagination_class=PageNumberPagination
    search_fields=('category_name',)
    def get_queryset(self):
        return ProductCategory.object.all()

    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)


    def get_object(self):
        obj = ProductCategory.object.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_child_categories(self, request, *args, **kwargs):
        try:
            product_category = self.get_object()
            child_categories = product_category.child_categories.all()
            serializer = ChildProductCategorySerializer(child_categories, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return 

    @action(detail=True, methods=['post'])
    def add_child_categories(self, request, *args, **kwargs):
        product_category = self.get_object()
        child_category_ids = request.data.get('child_categories', [])
        if not child_category_ids:
            product_category.child_categories.clear()
            serializer = self.serializer_class(product_category, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            child_categories = [ProductCategory.object.get_object_by_public_id(child_category_id) for child_category_id in child_category_ids]
            product_category.add_child_categories(*child_categories)
            serializer = self.serializer_class(product_category, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Child category not found"}, status=status.HTTP_404_NOT_FOUND)
            

    @action(detail=True, methods=['post'])
    def delete_child_category(self, request,  *args, **kwargs):
        parent_category = self.get_object()
        child_category_ids = request.data.get('child_categories', [])
        if not child_category_ids:
            return Response({"detail": "Child category public_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            child_categories = [ProductCategory.object.get_object_by_public_id(child_category_id) for child_category_id in child_category_ids]
            parent_category.delete_child(*child_categories)
            serializer=ProductCategorySerializer(parent_category,context={"request":request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ProductCategory.object.model.DoesNotExist:
            return Response({"detail": "Child category not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def delete_many_categories(self,request):
        categories = request.data.get('categories', [])
        try:
            ProductCategory.object.delete_many(categories)
            return Response({"detail": "DELETED"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'])
    def top_two(self, request):
        top_two_categories = self.get_queryset()[:2]
        serializer = self.get_serializer(top_two_categories, many=True)
        return Response(serializer.data)
        