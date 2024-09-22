from rest_framework import serializers
from ..abstract.serializers import AbstractSerializer
from ..size_option.models import SizeOption
from ..size_option.serializers import SizeOptionSerializer
from ..product_items.models import ProductItems
from .models import ProductVariation


class ProductVariationSerializer(AbstractSerializer):
    size_option = serializers.SlugRelatedField(queryset=SizeOption.object.all(), slug_field="public_id")
    product_items = serializers.SlugRelatedField(queryset=ProductItems.object.all(), slug_field="public_id")

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        size_option = SizeOption.object.get_object_by_public_id(rep["size_option"])
        rep['size_option'] = SizeOptionSerializer(size_option, context=self.context).data
        return rep

    class Meta:
        model = ProductVariation
        fields = '__all__'
        read_only_fields = ['edited']
