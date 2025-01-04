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


        # user = request.user
        #
        # profile = UserProfile.objects.get(userName=user)
        # posts = Post.objects.filter(owner=user)
        # profile_data = ProfileSerializer(profile).data
        # profile_data['posts'] = ProfileSerializer(posts,many=True).data
        # return Response(profile_data)



        # try:
        #     user_profile = UserProfile.objects.get(userName=user)
        #     serializer  = ProfileSerializer(user_profile)
        #     return  Response(serializer.data)
        # except UserProfile.DoesNotExist:
        #     return  Response({'error':'UserProfile Does not exits.'},status=404)



# class ProfileViewSet(APIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)