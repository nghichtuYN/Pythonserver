from rest_framework import serializers
from src.abstract.serializers import AbstractSerializer
from src.products.models import Products
from src.product_category.models import ProductCategory
from src.product_category.serializers import ProductCategorySerializer
from src.brand.models import Brand
from src.brand.serializers import BrandSerializer


# from rest_framework.exceptions import ValidationError


class ProductsSerializer(AbstractSerializer):
    product_category = serializers.SlugRelatedField(queryset=ProductCategory.object.all(), slug_field="public_id")
    brand = serializers.SlugRelatedField(queryset=Brand.object.all(), slug_field="public_id")
   

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True

        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        product_category = ProductCategory.object.get_object_by_public_id(rep["product_category"])
        rep["product_category"] = ProductCategorySerializer(product_category, context=self.context).data
        brand = Brand.object.get_object_by_public_id(rep['brand'])
        rep["brand"] = BrandSerializer(brand, context=self.context).data
        return rep
    
   
    class Meta:
        model = Products
        fields = "__all__"
        read_only_fields = ["edited"]
