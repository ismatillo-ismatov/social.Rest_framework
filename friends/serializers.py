from .models import FriendsRequest
from rest_framework import serializers
from django.contrib.auth.models import User


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendsRequest
        fields = ['request_from','request_to','status']