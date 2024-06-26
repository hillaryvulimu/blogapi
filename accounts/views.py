
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserProfileSerializer

class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
