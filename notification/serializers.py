from comments.serializers import CommentSerializer,ShortUserSerializer
from users.serializer import UserSerializer
from posts.serializers import PostSerializer
from votes.serializers import LikeSerializer
from .models import Notification
from django.contrib.auth.models import User
from user_profile.serializer import ProfileSerializer,MiniProfileSerializer
from rest_framework import serializers
from comments.models import Comment



class NotificationSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)
    like = LikeSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    # sender = ShortUserSerializer(read_only=True)
    # receiver = ShortUserSerializer(read_only=True)
    sender = MiniProfileSerializer(source='sender.profile',read_only=True)
    receiver = MiniProfileSerializer('receiver.profile',read_only=True)
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'is_read',
            'created_at',
            'sender',
            'receiver',
            'post',
            'comment',
            'like',
                  ]
        read_only_fields = ['is_read','created_at']


