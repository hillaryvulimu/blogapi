from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    profile_pic = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        
        data_dict['email'] = self.validated_data.get('email', '')
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')

        return data_dict
