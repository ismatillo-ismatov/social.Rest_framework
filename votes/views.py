from crypt import methods
from venv import create

from allauth.headless.base.views import APIView
from django.dispatch import receiver
# from django.contrib.admin import action
# from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from urllib3 import request

from posts.models import Post
from votes.permissions import VoteReadOnly
from django.shortcuts import get_object_or_404,render
from rest_framework import serializers,status,permissions,viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from notification.models import Notification

from .admin import Likes
from .models import Like
from .serializers import LikeSerializer




class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,VoteReadOnly]



    @action(detail=False,methods=['post'],url_path='toggle')
    def toggle_like(self,request):
        post_id = request.data.get('post')
        post_instance = get_object_or_404(Post,pk=post_id)
        like_instance = Like.objects.filter(post=post_instance,user=request.user).first()

        if like_instance:
            like_instance.delete()
            return Response({'message':'Like removed','liked':False},status=status.HTTP_200_OK)
        else:
            like = Like.objects.create(post=post_instance,user=request.user)


         

            return Response({'message':'Like added','liked':True,'like_id':like.id},status=status.HTTP_201_CREATED)