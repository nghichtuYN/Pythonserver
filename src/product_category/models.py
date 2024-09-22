from typing import Any
from django.db import models
from src.abstract.models import AbstractModel, AbstractManager


def category_directory_path(instance, filename):
    return "category_{0}/{1}".format(instance.public_id, filename)

class ProductCategoryManager(AbstractManager):
     def delete_many(self,categories):
        categories_to_delete=map(lambda x: x.public_id,[self.get_object_by_public_id(cateagory) for cateagory in categories])
        categories=self.filter(public_id__in=categories_to_delete)
        deleted_count, _ = categories.delete()
        return deleted_count

class ProductCategory(AbstractModel):
    category_name = models.TextField(max_length=255,blank=True,null=True)
    category_description = models.TextField(blank=True)
    edited = models.BooleanField(default=False)
    child_categories = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='parent_categories')
    size_category=models.ForeignKey("src_size_category.SizeCategory",on_delete=models.SET_NULL,null=True,default=None,blank=True)
    object = ProductCategoryManager()
    is_active=models.BooleanField(default=True)
    @property
    def name(self):
        return f"{self.category_name}"
    def is_sub_category(self, category):
        return self.child_categories.filter(pk=category.pk).exists()
    
    def add_child_categories(self, *categories):
        new_category_ids = [cat.pk for cat in categories]
        current_child_categories = self.child_categories.all()
        categories_to_add = [cat for cat in categories if not self.is_sub_category(cat)]
        categories_to_remove = current_child_categories.exclude(pk__in=new_category_ids)
        if categories_to_remove:
            self.child_categories.remove(*categories_to_remove)
        if categories_to_add:
            self.child_categories.add(*categories_to_add)
        return self
    
    def delete_child(self,*child_category):
        self.child_categories.remove(*child_category)
        return self