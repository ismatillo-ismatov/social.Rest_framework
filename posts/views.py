from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Post,Story,StoryMessage
from .serializers import PostSerializer,StorySerializer,StoryMessageSerializer
from user_profile.permissions import IsOwnerReadOnly
from .pagination import CustomPagination

class PostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return  Post.objects.filter(owner=user)
        return Post.objects.none()




    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


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
