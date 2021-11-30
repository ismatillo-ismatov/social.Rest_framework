from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Post
from .serializers import PostSerializer
from user_profile.permissions import IsOwnerReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)