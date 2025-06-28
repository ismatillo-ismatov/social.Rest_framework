from django.shortcuts import render
from rest_framework.permissions import AllowAny
from  rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CommentSerializer
from rest_framework import viewsets,status,permissions
from .models import Comment
from user_profile.permissions import IsOwnerReadOnly
from notification.models import Notification
from posts.pagination import CustomPagination

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id',None)
        if post_id is not None:
            return self.queryset.filter(post_id=post_id).prefetch_related('replies')
        return self.queryset.prefetch_related('replies')


    def perform_create(self, serializer):
        comment = serializer.save(owner=self.request.user)
        post_owner = comment.post.owner
        if post_owner != self.request.user:
            Notification.objects.create(
                sender=self.request.user,
                receiver=post_owner,
                notification_type='comment',
                post=comment.post,
                comment=comment,
            )
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

            if comment.owner != user:
                Notification.objects.create(
                    sender=user,
                    receiver=comment.owner,
                    notification_type='comment_like',
                    post=comment.post,
                    comment=comment,
                )
        return Response({'liked': liked, 'like_count': comment.like_count})



    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def reply(self, request, pk=None):
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reply_comment = serializer.save(
            owner=request.user,
            post=parent_comment.post,
            parent=parent_comment
        )
        if parent_comment.owner != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=parent_comment.owner,
                notification='reply',
                post=parent_comment.post,
                comment=reply_comment,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # @action(detail=True,methods=['POST'],permission_classes=[permissions.IsAuthenticated])
    # def reply(self,request,pk=None):
    #     parent_comment = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(
    #         owner=request.user,
    #         post=parent_comment.post,
    #         parent=parent_comment
    #     )
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)