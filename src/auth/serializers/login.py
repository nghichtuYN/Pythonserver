from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from src.user.serializers import UserSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = str(user.public_id).replace('-', '')
        token['is_admin']=user.is_superuser
        return token

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = MyTokenObtainPairSerializer.get_token(self.user)
        data["user"] = UserSerializer(self.user, context=self.context).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
