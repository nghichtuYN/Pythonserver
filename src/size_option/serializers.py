from src.abstract.serializers import AbstractSerializer
from src.size_option.models import SizeOption
from rest_framework import serializers
from src.size_category.models import SizeCategory
from src.size_category.serializers import SizeCategorySerializer

class SizeOptionSerializer(AbstractSerializer):
    size_category=serializers.SlugRelatedField(queryset=SizeCategory.objects.all(),slug_field="public_id")
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        size_category=SizeCategory.objects.get_object_by_public_id(rep['size_category'])
        rep['size_category']=SizeCategorySerializer(size_category,context=self.context).data
        return rep
    class Meta:
        model = SizeOption
        fields = '__all__'
        read_only_fields = ['edited']
