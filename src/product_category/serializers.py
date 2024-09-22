from rest_framework import serializers
from src.abstract.serializers import AbstractSerializer
from src.product_category.models import ProductCategory
from src.size_category.models import SizeCategory
from src.size_category.serializers import SizeCategorySerializer
class ChildProductCategorySerializer(AbstractSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"
        read_only_fields = ['edited']


class ProductCategorySerializer(AbstractSerializer):
    size_category=serializers.SlugRelatedField(queryset=SizeCategory.objects.all(),slug_field="public_id",required=False, allow_null=True )
    child_categories = serializers.SlugRelatedField(queryset=ProductCategory.object.all(), slug_field="public_id",
                                                    many=True,
                                                    required=False)

    class Meta:
        model = ProductCategory
        fields = "__all__"
        read_only_fields = ['edited']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["child_categories"] = ChildProductCategorySerializer(instance.child_categories.all(), many=True).data
    
        size_category_instance = SizeCategory.objects.get_object_by_public_id(rep["size_category"])
        if isinstance(size_category_instance, SizeCategory):
            rep['size_category'] = SizeCategorySerializer(size_category_instance, context=self.context).data
        else:
            rep['size_category'] = None
        return rep

    
    
    def get_child_categories(self, instance):
        request = self.context.get("request", None)
        if request is None:
            return False
        return request.product_category.has_child_categories(instance)

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data["edited"] = True
        instance = super().update(instance, validated_data)

        return instance
