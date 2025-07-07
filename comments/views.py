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
            return self.queryset.filter(post_id=post_id,parent=None).prefetch_related('replies')
        return self.queryset.filter(parent=None).prefetch_related('replies')


    def perform_create(self, serializer):
        comment = serializer.save(owner=self.request.user)
        if comment.parent and comment.parent.owner != self.request.user:
            Notification.objects.create(
                sender=self.request.user,
                receiver=comment.parent.owner,
                notification_type='reply',
                post=comment.post,
                comment=comment,
            )

        elif comment.post and comment.post.owner != self.request.user:
            Notification.objects.create(
                sender=self.request.user,
                receiver=comment.post.owner,
                notification_type='comment',
                post=comment.post,
                comment=comment,
            )




    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['POST'],permission_classes=[permissions.IsAuthenticated])
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
        return Response({'is_liked': liked, 'like_count': comment.likes.count()})



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


