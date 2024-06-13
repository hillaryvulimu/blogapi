
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Post, Comment, LikeDislike

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = get_user_model()
        fields = ("id", "username", 'first_name', 'last_name') # Also be send to front-end


class CommentSerializer(serializers.ModelSerializer):
    commenter = UserSerializer()  # Serialize the User model fields for the commenter
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'commenter', 'text', 'created_at')


class LikeDislikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Serialize the User model fields for the user
    
    class Meta:
        model = LikeDislike
        fields = ('id', 'post', 'user', 'reaction')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Serialize the User model fields for the author
    comments = CommentSerializer(many=True, read_only=True)  # Serialize comments related to the post
    likes_dislikes = LikeDislikeSerializer(many=True, read_only=True)  # Serialize likes/dislikes related to the post
    
    class Meta:
        model = Post
        fields = '__all__' # ( "id", "author", "title", "body", "created_at", "post_pic", )


