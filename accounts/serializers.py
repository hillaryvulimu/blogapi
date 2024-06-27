
from rest_framework import serializers
from .models import CustomUser


# serializer for views
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic']
        read_only_fields = ['username', 'email']


# serializer for viewset
class UserProfileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic']
        read_only_fields = ['username', 'email']


class UserProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_pic']

    def update(self, instance, validated_data):
        # Handle password change separately
        instance = super().update(instance, validated_data)
        return instance