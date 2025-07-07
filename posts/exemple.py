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
