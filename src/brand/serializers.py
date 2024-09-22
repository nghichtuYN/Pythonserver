from ..abstract.serializers import AbstractSerializer
from .models import Brand


class BrandSerializer(AbstractSerializer):
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Brand
        fields = '__all__'
        read_only_fields = ['edited']
