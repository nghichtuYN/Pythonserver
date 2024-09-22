from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny
from src.abstract.viewsets import AbstractViewSet
from src.size_option.serializers import SizeOptionSerializer
from src.size_option.models import SizeOption
from rest_framework.decorators import action
from src.size_category.models import SizeCategory
from rest_framework.pagination import PageNumberPagination

class SizeOptionViewSet(AbstractViewSet):
    http_method_names = ("post", "put", "get", "delete")
    permission_classes = (AllowAny,)
    serializer_class = SizeOptionSerializer
    pagination_class=PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SizeOption.objects.all()

        size_category_pk = self.kwargs["size_category_pk"]
        if size_category_pk is None:
            return Http404
        queryset = SizeOption.object.filter(size_category__public_id=size_category_pk)

        return queryset

    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)


    def get_object(self):
        obj = SizeOption.object.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=False, methods=['post'])
    def delete_many_size_options(self,request):
            size_options = request.data.get('size_options', [])
            try:
                SizeOption.object.delete_many(size_options)
                return Response({"detail": "DELETED"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def add_size_options_by_size_category(self,request):
        size_category=request.data.get('size_category',"")
        size_options=request.data.get('size_options',[])
        try:
            size_category_obj=SizeCategory.objects.get_object_by_public_id(size_category)
            for size_option in size_options:
                SizeOption.object.create(size_category=size_category_obj,size_name=size_option)

            return Response({"detail": "CREATED"}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
