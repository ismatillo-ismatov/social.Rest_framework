from urllib3 import request

from .models import FriendsRequest
from rest_framework import serializers
from user_profile.models import UserProfile
from django.contrib.auth.models import User


class FriendRequestSerializer(serializers.ModelSerializer):
    request_from = serializers.PrimaryKeyRelatedField(read_only=True)
    request_to = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    # request_to = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),source='request_to.userName')



    class Meta:
        model = FriendsRequest
        fields = ['request_from','request_to','status']
        read_only_fields = ['request_from']


    def get_request_to(self,obj):
        # user = obj.request_to.userName
        return {
            "id": obj.request_to.userName.id,
            "username": obj.request_to.userName.username,
            "email": obj.request_to.userName.email,
        }

    # def create(self,validated_data):
    #     validated_data['request_from'] = self.context['request'].user.profile
    #     return super().create(validated_data)