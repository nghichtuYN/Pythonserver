from django.apps import AppConfig


class ProductImageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.product_image'
    label = 'src_product_image'
    
    def ready(self):
        import src.product_image.signals
    