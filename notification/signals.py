from django.template.defaultfilters import title
from .utils import send_notification

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.defaulttags import comment
from django.contrib.auth.models import User
from fcm.fcm import send_push_notification
from votes.models import Like
from notification.models import Notification
from comments.models import Comment



def send_test_notification(token,title,body):
    token = "usqfk8ARuKO8znuSbI9_L:APA91bF5OjaakuJQpFRTO_V4aIxvqb-xQ_PKo-0m8rAtt540SZHGxnFVB75vIENxV8F1mzoR8RL2ztMrzDbCOtRSANLo8JSZC7oTQ44aECGbdr6OZ_k96uk"
    title = "yangilik"
    body="Bizda yangi mahsulotlar bor!"
    try:
        response = send_push_notification(title,body,token)
        print("✅ Notification yuborildi:", response)
    except Exception as e:
        print("❌ Xatolik:", e)


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
        token = instance.owner.profile.fcm_token if hasattr(instance.post.owner,'profile') else None
        if token:
            send_notification(token,'Yoqtirish',f"{instance.user.username} sizning postingni yoqtirdi")


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
            token = parent_owner.profile.fcm_token if hasattr(parent_owner,'profile') else None
            if token:
                send_notification(
                    token,
                    title="yangi javob",
                    body=f"{instance.owner.username}sizning izohingizga jabob berdi"
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
            token = post_owner.profile.fcm_token if hasattr(post_owner, 'profile') else None
            if token:
                send_notification(
                    token,
                    title="yangi javob",
                    body=f"{instance.owner.username}sizning postingizga izoh yozdi "
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
                token = instance.owner.profile.fcm_token if hasattr(instance.post.owner, 'profile') else None
                if token:
                    send_notification(token, 'Yoqtirish', f"{instance.user.username} sizning postingni yoqtirdi")
