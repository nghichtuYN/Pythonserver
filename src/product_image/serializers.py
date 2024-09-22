from rest_framework import serializers
from src.abstract.serializers import AbstractSerializer
from .models import ProductImage
from src.product_items.models import ProductItems
from django.core.files.storage import default_storage


class ProductImageSerializer(AbstractSerializer):
    product_items = serializers.SlugRelatedField(queryset=ProductItems.object.all(), slug_field="public_id")
    def update(self, instance, validated_data):
        old_image = instance.image_filename

        instance = super().update(instance, validated_data)

        if old_image and old_image != instance.image_filename:
            old_image_path = old_image
            if default_storage.exists(old_image_path):
                default_storage.delete(old_image_path)

        if not instance.edited:
            instance.edited = True
            instance.save()

        return instance

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     product_items = ProductItems.object.get_object_by_public_id(rep["product_items"])
    #     rep["product_items"] = ProductItemsSerializer(product_items, context=self.context).data
    #     return rep
    
            
    class Meta:
        model = ProductImage
        fields = ['id',"product_items",'image_filename']
        read_only_fields = ['edited']
