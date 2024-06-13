from django.test import TestCase

from django.contrib.auth import get_user_model

from django.utils.text import slugify

from django.urls import reverse

from rest_framework import serializers
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from .models import Post, Comment, LikeDislike

from datetime import datetime
from .views import UserViewSet, PostViewSet

from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeDislikeSerializer

User = get_user_model()

# Model tests
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            first_name = 'Test',
            last_name = 'User',
            email="test@email.com",
            password="secret",
        )

        cls.post = Post.objects.create(
            author=cls.user,
            title="A good title",
            body="Nice body content",
            category=Post.Category.CARD  # Test specific category
        )
        
        cls.comment = Comment.objects.create(
            post=cls.post,
            commenter=cls.user,
            text="This is a test comment."
        )

        cls.like = LikeDislike.objects.create(
            post=cls.post,
            user=cls.user,
            reaction=LikeDislike.Reaction.LIKE
        )

    def test_post_model(self):
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.title, "A good title")
        self.assertEqual(self.post.body, "Nice body content")
        self.assertEqual(self.post.category, Post.Category.CARD)  # Test category field
        self.assertEqual(self.post.slug, slugify(self.post.title))  # Test slug field
        self.assertEqual(str(self.post), "A good title")

    def test_comment_model(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.commenter, self.user)
        self.assertEqual(self.comment.text, "This is a test comment.")
        self.assertIn(str(self.user), str(self.comment))  # Check commenter in __str__

    def test_like_dislike_model(self):
        self.assertEqual(self.like.post, self.post)
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.reaction, LikeDislike.Reaction.LIKE)
        self.assertIn(str(self.user), str(self.like))  # Check user in __str__


# Serializers tests
# users serializer
class UserSerializerTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_user_serializer(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user_obj = serializer.save()
        self.assertIsInstance(user_obj, User)

# comments serializer
class CommentSerializer(serializers.ModelSerializer):
    # lookup existing user by id instead of creating a new one when one's available
    commenter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'commenter', 'text', 'created_at')


class CommentSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='commenter', first_name='Test', last_name='User')
        self.post = Post.objects.create(title='Test Post', body='Test content', author=self.user)
        self.comment_data = {
            'post': self.post.id,
            'commenter': self.user.id,  # Use the user ID
            'text': 'Test comment',
            'created_at': datetime.now(),
        }

    def test_comment_serializer(self):
        serializer = CommentSerializer(data=self.comment_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        comment_obj = serializer.save()
        self.assertIsInstance(comment_obj, Comment)


# likes/dislikes serializer
class LikeDislikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = LikeDislike
        fields = ('id', 'post', 'user', 'reaction')


class LikeDislikeSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='liker', first_name='John', last_name='Doe')
        self.post = Post.objects.create(title='Test Post', body='Test content', author=self.user)
        self.like_dislike_data = {
            'post': self.post.id,
            'user': self.user.id,  # Use the user ID
            'reaction': 'Like',
        }

    def test_like_dislike_serializer(self):
        serializer = LikeDislikeSerializer(data=self.like_dislike_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        like_dislike_obj = serializer.save()
        self.assertIsInstance(like_dislike_obj, LikeDislike)


# posts serializer
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comments = CommentSerializer(many=True, read_only=True)
    likes_dislikes = LikeDislikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "title", "body", "created_at", "comments", "likes_dislikes")


class PostSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='author', first_name='John', last_name='Doe')
        self.post_data = {
            'author': self.user.id,  # Use the user ID
            'title': 'Test Post',
            'body': 'Test content',
            'created_at': datetime.now(),
        }

    def test_post_serializer(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        post_obj = serializer.save()
        self.assertIsInstance(post_obj, Post)
