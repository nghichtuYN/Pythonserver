from django.db import models
from src.abstract.models import AbstractModel, AbstractManager


class SizeOptionManager(AbstractManager):
    def delete_many(self,size_options):
        size_options_delete=map(lambda x: x.public_id,[self.get_object_by_public_id(size_option) for size_option in size_options])
        size_option=self.filter(public_id__in=size_options_delete)
        deleted_count, _ = size_option.delete()
        return deleted_count


class SizeOption(AbstractModel):
    size_name = models.TextField(max_length=255)
    size_category=models.ForeignKey("src_size_category.SizeCategory",on_delete=models.SET_NULL,null=True)
    edited = models.BooleanField(default=False)
    object = SizeOptionManager()
