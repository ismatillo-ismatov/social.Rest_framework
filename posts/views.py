from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Post,Story
from .serializers import PostSerializer,StorySerializer
from user_profile.permissions import IsOwnerReadOnly
from .pagination import CustomPagination

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]
    pagination_class = CustomPagination





    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]