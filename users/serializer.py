from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import  status
from user_profile.models import UserProfile
from posts.serializers import PostSerializer
from urllib3 import request
from user_profile.serializer import ProfileSerializer
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer(read_only=True)
    ownerProfileImage = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username','password','email','userprofile','ownerProfileImage','posts']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(userName=user)
        return user


    def get_ownerProfileImage(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profileImage:
            return obj.profile.profileImage.url
        return None

    def get_posts(self,obj):
        if hasattr(obj,'posts'):
            return  PostSerializer(obj.posts.all(),many=True).data
        return []

    # def get_posts(self, obj):
    #     return PostSerializer(obj.user.posts.all(), many=True).data
