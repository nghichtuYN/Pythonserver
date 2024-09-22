#signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from src.product_image.models import ProductImage
from src.product_items.models import ProductItems
import os
from django.conf import settings
import shutil 
@receiver(pre_delete, sender=ProductItems)
def delete_related_images(sender, instance, **kwargs):
    images = ProductImage.object.filter(product_items=instance)
    folder_path = os.path.join(settings.MEDIA_ROOT, f"productItems_{instance.public_id}")
        
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder_path}")
    images.delete()
