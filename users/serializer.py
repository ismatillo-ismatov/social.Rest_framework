from django.views.decorators.csrf import csrf_exempt
from drf_yasg.openapi import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import  status
from urllib3 import request
from user_profile.serializer import ProfileSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    profile_data = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id','username','email','password','is_active','profile_data')
        extra_kwargs={"email":{"required":True,'write_only':True},'password':{"write_only":True}}


    def create(self,validated_data):

        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )

        user.set_password(validated_data["password"])
        user.save()
        return user