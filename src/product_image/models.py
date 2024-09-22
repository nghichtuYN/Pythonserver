from django.db import models
from src.abstract.models import AbstractModel, AbstractManager


def product_directory_path(instance, filename):
    return "productItems_{0}/{1}".format(instance.product_items.public_id, filename)


class ProductImageManager(AbstractManager):
    pass


class ProductImage(AbstractModel):
    product_items = models.ForeignKey("src_product_items.ProductItems", on_delete=models.CASCADE,null=True)
    image_filename = models.ImageField(upload_to=product_directory_path, blank=True, null=True,default=None)
    edited = models.BooleanField(default=False)
    object = ProductImageManager()
