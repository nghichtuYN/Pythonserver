from rest_framework import serializers
from src.user.models import User
from src.user.serializers import UserSerializer

class GoogleSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "avatar",
            "email",
            "first_name",
            "last_name",
            "password",
        ]

    def create(self, validated_data):
        return User.objects.create_google_user(**validated_data)
