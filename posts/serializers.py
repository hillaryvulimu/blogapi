
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Post

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = get_user_model()
        fields = ("id", "username", 'first_name', 'last_name') # to send to front-end


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Serialize the User model fields
    class Meta:
        model = Post
        fields = '__all__' # ( "id", "author", "title", "body", "created_at", "post_pic", )


