from cgitb import reset
from django.shortcuts import render
from django.utils.termcolors import RESET
from rest_framework.response import Response
from rest_framework import viewsets,permissions
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from websockets import serve

from user_profile.models import UserProfile
from votes.models import Like
from .models import Post,Story,StoryMessage
from friends.models import FriendsRequest
from django.db.models import Q
from .serializers import PostSerializer,StorySerializer,StoryMessageSerializer
from user_profile.permissions import IsOwnerReadOnly
from .pagination import CustomPagination


import boto3
from django.conf import settings

def upload_to_s3(local_file_path, s3_file_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    s3.upload_file(
        local_file_path,
        settings.AWS_STORAGE_BUCKET_NAME,
        s3_file_name,
    )
    file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_file_name}"
    return  file_url

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]
    pagination_class = CustomPagination
    parser_classes = [MultiPartParser,FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return  Post.objects.filter(owner=user)
        return Post.objects.none()



    @action(detail=True,methods=['post'],permission_classes=[IsAuthenticated])
    def toggle_like(self,request, pk=None):
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(user=request.user,post=post)
        if created:
            return Response({"message":"Post liked"},status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({"message":"Post unliked"},status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()



    @action(detail=False,methods=['get'],url_path='friends',permission_classes=[IsAuthenticated])
    def friend_posts(self,request):
        user = request.user
        user_profile = UserProfile.objects.get(userName=user)
        accepted_requests = FriendsRequest.objects.filter(
            (Q(request_from=user_profile) | Q(request_to=user_profile)) & Q(status='Accepted')
        )
        friend_users =[
            fr.request_to.userName if fr.request_from == user_profile else fr.request_from.userName
            for fr in accepted_requests
        ]

        posts = Post.objects.filter(owner__in=friend_users).order_by('-post_date')
        serializer = self.get_serializer(posts,many=True,context={'request':request})
        return  Response(serializer.data)



class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_class = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)



class StoryMessageViewSet(viewsets.ModelViewSet):
    queryset = StoryMessage.objects.all()
    serializer_class = StoryMessageSerializer
    permission_class = [permissions.IsAuthenticated,IsOwnerReadOnly]

    def perform_class(self,serializer):
        serializer.save(sender=self.request.user)
