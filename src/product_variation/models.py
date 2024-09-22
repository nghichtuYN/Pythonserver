from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


class ProductVariationManager(AbstractManager):
    pass


class ProductVariation(AbstractModel):
    product_items = models.ForeignKey("src_product_items.ProductItems", on_delete=models.CASCADE)
    size_option = models.ForeignKey("src_size_option.SizeOption", on_delete=models.CASCADE,null=True,blank=True,default=None)
    qty_in_stock = models.BigIntegerField(default=0)
    edited = models.BooleanField(default=False)
    object = ProductVariationManager()
