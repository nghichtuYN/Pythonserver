from src.abstract.serializers import AbstractSerializer
from src.order_items.models import OrderItems
from rest_framework import serializers
from src.product_items.models import ProductItems
from src.orders.models import Orders
from src.product_items.serializers import ProductItemsSerializer
from src.product_variation.models import ProductVariation
from src.product_variation.serializers import ProductVariationSerializer
class OrderItemsSerializer(AbstractSerializer):
    orders=serializers.SlugRelatedField(queryset=Orders.object.all(),slug_field="public_id")
    product_item=serializers.SlugRelatedField(queryset=ProductItems.object.all(),slug_field="public_id")
    product_variation=serializers.SlugRelatedField(queryset=ProductVariation.object.all(),slug_field="public_id")
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data["edited"] = True

        instance = super().update(instance, validated_data)

        return instance
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        product_item = ProductItems.object.get_object_by_public_id(rep["product_item"])
        product_variation = ProductVariation.object.get_object_by_public_id(rep["product_variation"])
        rep["product_item"] = ProductItemsSerializer(product_item, context=self.context).data
        if product_variation:
            rep["product_variation"] = ProductVariationSerializer(product_variation, context=self.context).data
        return rep
    
    class Meta:
        model=OrderItems
        fields = '__all__'
        read_only_fields = ['edited']
        

