from rest_framework import serializers
from src.user.models import User
from src.user.serializers import UserSerializer

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "avatar",
            "email",
            # "username",
            "first_name",
            "last_name",
            "password",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
