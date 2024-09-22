from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


class BrandManager(AbstractManager):
    pass


class Brand(AbstractModel):
    brand_name = models.CharField(db_index=True, unique=True, max_length=255)
    brand_description = models.TextField(blank=True, null=True)
    edited = models.BooleanField(default=False)
    object = BrandManager()

    def __str__(self):
        return f"{self.brand_name}"
# Create your models here.
