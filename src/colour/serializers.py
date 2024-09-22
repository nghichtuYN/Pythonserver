from ..abstract.serializers import AbstractSerializer
from .models import Colour


class ColourSerializer(AbstractSerializer):
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data["edited"] = True
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Colour
        fields = ['id','colour_name','hex_code']
