from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from posts.models import Story
# from  user_profile.serializer import ProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='id', queryset=UserProfile.objects.all())
    receiver = serializers.SlugRelatedField(slug_field='id', queryset=UserProfile.objects.all())
    # sender = serializers.SlugRelatedField(slug_field='userName',queryset=UserProfile.objects.all())
    # receiver = serializers.SlugRelatedField(slug_field='userName',queryset=UserProfile.objects.all())
    # sender = serializers.SlugRelatedField(many=False, slug_field="username", queryset=User.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ["id","sender","receiver", "message", "timestamp",'is_read',]


