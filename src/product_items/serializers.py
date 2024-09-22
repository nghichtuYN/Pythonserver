from src.abstract.serializers import AbstractSerializer
from src.product_items.models import ProductItems
from rest_framework import serializers
from src.products.models import Products
from src.products.serializers import ProductsSerializer
from src.colour.serializers import ColourSerializer
from src.colour.models import Colour
from src.product_image.models import ProductImage
from src.size_option.models import SizeOption
from src.product_variation.models import ProductVariation
from src.product_image.serializers import ProductImageSerializer
from src.product_variation.serializers import ProductVariationSerializer

class ProductItemsSerializer(AbstractSerializer):
    product = serializers.SlugRelatedField(queryset=Products.object.all(), slug_field="public_id")
    colour = serializers.SlugRelatedField(queryset=Colour.object.all(), slug_field="public_id")
    image_filename=serializers.ListField(child=serializers.ImageField(max_length=100000,allow_empty_file=False,use_url=False),write_only=True)
    qty_in_stock=serializers.FloatField(write_only=True)
    size_option=serializers.CharField(write_only=True)
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data["edited"] = True

        instance = super().update(instance, validated_data)

        return instance

    def to_representation(self, instance):
        
        rep = super().to_representation(instance)
        product = Products.object.get_object_by_public_id(rep["product"])
        colour = Colour.object.get_object_by_public_id(rep["colour"])
        rep["product"] = ProductsSerializer(product, context=self.context).data
        rep["colour"] = ColourSerializer(colour, context=self.context).data
        product_images = ProductImage.object.filter(product_items=instance)
        product_variations = ProductVariation.object.filter(product_items=instance)
        rep["images"] = ProductImageSerializer(product_images, many=True, context=self.context).data
        rep["variations"] = ProductVariationSerializer(product_variations, many=True, context=self.context).data

        return rep
    
    def create(self, validated_data):
        image_filenames=validated_data.pop("image_filename")
        size_option_id=validated_data.pop('size_option')
        qty_in_stock=validated_data.pop('qty_in_stock')
        size_option = SizeOption.object.get_object_by_public_id(size_option_id)
        product_items=ProductItems.object.create(**validated_data)
        for image in image_filenames:
            ProductImage.object.create(product_items=product_items,image_filename=image)
        ProductVariation.object.create(product_items=product_items,size_option=size_option,qty_in_stock=qty_in_stock)
        return product_items
    class Meta:
        model = ProductItems
        fields = '__all__'
        read_only_fields = ['edited']
