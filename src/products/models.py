from django.db import models
from src.abstract.models import AbstractModel, AbstractManager


class ProductsManager(AbstractManager):
    def delete_many(self,products):
        products_to_delete=map(lambda x: x.public_id,[self.get_object_by_public_id(product) for product in products])
        products=self.filter(public_id__in=products_to_delete)
        deleted_count, _ = products.delete()
        return deleted_count


class Products(AbstractModel):
    product_name = models.TextField(max_length=255)
    product_description = models.TextField(blank=True, null=True)
    edited = models.BooleanField(default=True)
    product_category = models.ForeignKey("src_product_category.ProductCategory", on_delete=models.CASCADE)
    brand = models.ForeignKey("src_brand.Brand", on_delete=models.CASCADE, default=None)

    object = ProductsManager()
