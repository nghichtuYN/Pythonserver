from rest_framework.permissions import IsAuthenticated

from src.abstract.viewsets import AbstractViewSet
from src.user.serializers import UserSerializer
from src.user.models import User
from src.auth.permissions import UserPermission

class UserViewSet(AbstractViewSet):
    http_method_names = ("patch", "get")
    permission_classes = (
        IsAuthenticated,
        UserPermission,
    )
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj