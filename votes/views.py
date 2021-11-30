from posts.models import Post
from votes.permissions import VoteReadOnly
from django.shortcuts import get_object_or_404,render
from rest_framework import serializers,status,permissions,viewsets
from .models import Vote
from .serializers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,VoteReadOnly]

    def perform_create(self, serializer):
        post_instance = get_object_or_404(Post,pk=self.request.data["post"])
        if self.request.data['up_vote']:
            already_up_voted = Vote.objects.filter(post=post_instance,up_vote_by=self.request.user).exists()
            if already_up_voted:
                raise serializers.ValidationError({"message":"you have already liked this post"})
            else:
                serializer.save(up_vote_by=self.request.user,post=post_instance)

        else:
            already_down_voted = Vote.objects.filter(post=post_instance,down_vote_by=self.request.user).exists()
            if already_down_voted:
                raise serializers.ValidationError({"massage":"you have already dislike this post"})
            else:
                serializer.save(down_voted_by=self.request.user,post=post_instance)