from src.abstract.serializers import AbstractSerializer
from src.size_category.models import SizeCategory
from src.size_option.models import SizeOption
from rest_framework import serializers
class SizeCategorySerializer(AbstractSerializer):
    size_options=serializers.ListField(child=serializers.CharField(max_length=255),write_only=True,required=False)
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance
    def create(self, validated_data):
        size_options=validated_data.pop("size_options")
        size_category=SizeCategory.objects.create(**validated_data)
        for option in size_options:
            SizeOption.object.create(size_category=size_category,size_name=option)
        return size_category
    class Meta:
        model = SizeCategory
        fields = '__all__'
        read_only_fields = ['edited']