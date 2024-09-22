from django.db import models
from src.abstract.models import AbstractModel, AbstractManager

class OrderItemsManager(AbstractManager):
    pass

class OrderItems(AbstractModel):
    qty=models.IntegerField(default=0)
    price=models.FloatField(default=0)
    product_item=models.ForeignKey('src_product_items.ProductItems',on_delete=models.SET_NULL,null=True)
    orders=models.ForeignKey('src_orders.Orders',on_delete=models.CASCADE)
    product_variation =models.ForeignKey('src_product_variation.ProductVariation',on_delete=models.SET_NULL, null=True)
    edited=models.BooleanField(default=False)
    object=OrderItemsManager()
    