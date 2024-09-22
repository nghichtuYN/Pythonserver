from django.db import models
from src.abstract.models import AbstractModel, AbstractManager


class ProductItemsManager(AbstractManager):
    def delete_many(self,productItems):
        productItems_to_delete=map(lambda x: x.public_id,[self.get_object_by_public_id(productItem) for productItem in productItems])
        productItems=self.filter(public_id__in=productItems_to_delete)
        deleted_count, _ = productItems.delete()
        return deleted_count


class ProductItems(AbstractModel):
    product = models.ForeignKey("src_products.Products", on_delete=models.CASCADE)
    colour = models.ForeignKey("src_colour.Colour", on_delete=models.CASCADE)
    original_price = models.FloatField(null=True,blank=True)
    sale_price = models.FloatField(null=True, blank=True)
    object = ProductItemsManager()
    edited = models.BooleanField(default=False)
