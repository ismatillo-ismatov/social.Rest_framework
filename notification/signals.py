from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.defaulttags import comment
from django.contrib.auth.models import User

from votes.models import Like
from notification.models import Notification
from comments.models import Comment

@receiver(post_save,sender=Like)
def create_notification_on_like(sender,instance,created,**kwargs):
    if created and instance.post.owner != instance.user:
        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.owner,
            post=instance.post,
            notification_type='like',
            like=instance
        )


@receiver(post_save,sender=Comment)
def create_notification_on_comment(sender,instance,created,**kwargs):
    if not created:
        return

    if instance.parent:
        parent_owner = instance.parent.owner
        if parent_owner != instance.owner:
            Notification.objects.create(
                sender=instance.owner,
                receiver=parent_owner,
                post=instance.post,
                notification_type='reply',
                comment=instance
            )
    else:
        post_owner = instance.post.owner
        if post_owner != instance.owner:
            Notification.objects.create(
                sender=instance.owner,
                receiver=post_owner,
                post=instance.post,
                notification_type='comment',
                comment=instance
            )



@receiver(m2m_changed,sender=Comment.likes.through)
def create_notification_on_comment_like(sender,instance,action,pk_set,**kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            if instance.owner != user:
                Notification.objects.create(
                    sender=user,
                    receiver=instance.owner,
                    post=instance.post,
                    notification_type='comment_like',
                    comment=instance
                )
