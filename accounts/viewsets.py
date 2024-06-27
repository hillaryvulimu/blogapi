from rest_framework import viewsets, permissions, mixins
from .models import CustomUser
from .serializers import UserProfileReadSerializer, UserProfileWriteSerializer

class UserProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'update':
            return UserProfileWriteSerializer
        return UserProfileReadSerializer # other methods like retrieve

    def get_object(self):
        return self.request.user
