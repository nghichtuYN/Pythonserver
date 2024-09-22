from rest_framework import serializers
from src.abstract.serializers import AbstractSerializer
from src.user.models import User

class UserSerializer(AbstractSerializer):
    class Meta:
        model=User
        fields="__all__"
        read_only_field = ["is_active"]