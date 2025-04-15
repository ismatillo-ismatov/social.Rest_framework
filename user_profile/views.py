from os.path import defpath

from django.contrib.admin import action
from django.contrib.staticfiles.views import serve
from django.utils.termcolors import RESET
from drf_yasg.openapi import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from user_profile.serializer import ProfileSerializer
from user_profile.models import UserProfile
from posts.models import Post
from django.shortcuts import render
from rest_framework.response import Response
from .permissions import IsOwnerReadOnly
from rest_framework import viewsets,permissions


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        profile = UserProfile.objects.get(userName=request.user)
        serializer = ProfileSerializer(profile)
        return  Response(serializer.data)


