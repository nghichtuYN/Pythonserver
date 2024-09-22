from rest_framework import serializers
from src.abstract.serializers import AbstractSerializer
from src.orders.models import Orders
from src.user.models import User
from src.order_items.models import OrderItems
from src.product_items.models import ProductItems
from src.product_variation.models import ProductVariation
from src.order_items.serializers import OrderItemsSerializer
class OrderSerializer(AbstractSerializer):
    user=serializers.SlugRelatedField(queryset=User.objects.all(),slug_field="public_id",required=False)
    order_items=serializers.ListField(write_only=True,required=False)

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True

        instance = super().update(instance, validated_data)
        return instance
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        orderItems=OrderItems.object.filter(orders=instance)
        rep["orderItem"] = OrderItemsSerializer(orderItems, many=True, context=self.context).data
        return rep
    
    def create_order_items(self, order, order_items_data):
        for item_data in order_items_data:
            qty = item_data.get('amount')
            product_item = ProductItems.object.get_object_by_public_id(item_data.get('product'))
            price = item_data.get('price')
            size_option_id = item_data.get('size')
            product_variation = ProductVariation.object.get_object_by_public_id(size_option_id)
            print(product_variation)
            if product_variation:
                product_variation.qty_in_stock = max(product_variation.qty_in_stock - qty, 0) 
                product_variation.save()

            OrderItems.object.create(orders=order, product_item=product_item, qty=qty, price=price,product_variation=product_variation)
    
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Orders.object.create(**validated_data)
        self.create_order_items(order, order_items_data)

        return order
    
    class Meta:
        model=Orders
        fields="__all__"
        read_only_fields = ["edited"]
        