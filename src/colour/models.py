from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


class ColourManager(AbstractManager):
    pass


class Colour(AbstractModel):
    colour_name = models.TextField(max_length=20)
    hex_code=models.CharField(max_length=7,default=None,null=True,blank=True)
    edited = models.BooleanField(default=False)
    object = ColourManager()
