from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from src.auth.serializers import LoginSerializer, GoogleSerializer
from src.user.models import User

class GoogleLoginViewSet(ViewSet):
    serializer_class = GoogleSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()

        if not user:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save() 
                login_serializer = LoginSerializer(data=request.data, context={"request": request})
                try:
                    login_serializer.is_valid(raise_exception=True)
                except TokenError as e:
                    raise InvalidToken(e.args[0])
                return Response(login_serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = LoginSerializer(data=request.data, context={"request": request})
            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
