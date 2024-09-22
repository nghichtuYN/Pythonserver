from django.db import models
from src.abstract.models import AbstractModel, AbstractManager

class OrderManager(AbstractManager):
    pass
class Orders(AbstractModel):
    cus_name=models.CharField(max_length=255)
    cus_address=models.CharField(max_length=255)
    cus_email=models.EmailField(max_length=255)
    cus_phone = models.CharField(max_length=12 ,default=None)
    ord_cost=models.FloatField(default=0)
    edited = models.BooleanField(default=False)
    isPaid=models.BooleanField(default=False)
    user=models.ForeignKey("src_user.User",on_delete=models.CASCADE)
    
    object=OrderManager()
    