from django.db import models
from src.abstract.models import AbstractModel,AbstractManager

class SizeCategoryManager(AbstractManager):
    def delete_many(self,size_categories):
        size_categories_delete=map(lambda x: x.public_id,[self.get_object_by_public_id(size_category) for size_category in size_categories])
        size_category=self.filter(public_id__in=size_categories_delete)
        deleted_count, _ = size_category.delete()
        return deleted_count
class SizeCategory(AbstractModel):
    category_name=models.CharField(max_length=255)
    objects=SizeCategoryManager()
    edited=models.BooleanField(default=False)
    objects=SizeCategoryManager()
    