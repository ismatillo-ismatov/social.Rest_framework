from chat.models import Message
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
        recipient =  instance.post.owner
        print(f"Post egasi: {recipient.username} (ID: {recipient.id})")
        Notification.objects.create(
            sender=instance.user,
            receiver=recipient,
            post=instance.post,
            notification_type='like',
            like=instance
        )
        token=None
        if hasattr(recipient,'profile') and recipient.profile.fcm_token:
            token = recipient.profile.fcm_token
            print(f"FCM token{token}(Post Egasi: {recipient.username}) ")
        else:
            print(f"Xato: {recipient.username} uchun FCM token topilmadi")
            return
        try:
            send_push_notification(
                    title='Yoqtirish',
                    body=f"{instance.user.username} sizning postingizga yoqtirdi",
                    token=token,
                    data={
                        "notification_type":"like",
                        "post_id": str(instance.post.id),
                        "sender_id":str(instance.user.id),
                        "receiver_id":str(recipient.id)
                    }
               )

            print(f"Bildirishnoma yuborildi: {receiver.username} ga")
        except Exception as e:
                print(f"Xato: Bildirishnoma yuborishda muammo: {e}")





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
            token = None
            if hasattr(parent_owner,'profile') and parent_owner.profile and parent_owner.profile.fcm_token:
                token = parent_owner.profile.fcm_token
                print(f"FCM token: {token} (Izoh egasi: {parent_owner.username})")
            else:
                print(f"Xato: {parent_owner.username} uchun FCM token topilmadi")
                return

            try:
                send_push_notification(
                        title='yangi javob',
                        body=f"{instance.owner.username} sizning postingizga izoh javob yozdi",
                        token=token,
                        data={
                            "notification_type": "reply",
                            "post_id": str(instance.post.id),
                            "comment_id":str(instance.id),
                            "sender_id": str(instance.owner.id),
                            "receiver_id": str(parent_owner.id)
                        }
                    )
                print(f"Bildirishnoma yuborildi: {parent_owner.username} ga")
            except Exception as e:
                print(f"Xato: Bildirishnoma yuborishda muammo: {e}")

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
            token = None
            if hasattr(post_owner,'profile') and post_owner.profile  and post_owner.profile.fcm_token:
                token = post_owner.profile.fcm_token
                print(f"FCM token: {token} (Post egasi: {post_owner.username})")
            else:
                print(f"Xato: {post_owner.username} uchun FCM token topilmadi")
                return
            try:
                send_push_notification(
                        title='yangi izoh',
                        body=f"{instance.owner.username} sizning postingizga izoh yozdi",
                        token=token,
                        data={
                            "notification_type": "comment",
                            "post_id": str(instance.post.id),
                            "comment_id": str(instance.id),
                            "sender_id": str(instance.owner.id),
                            "receiver_id": str(post_owner.id)
                        }
                    )
                print(f"Bildirishnoma yuborildi: {post_owner.username} ga")
            except Exception as e:
                print(f"Xato: Bildirishnoma yuborishda muammo: {e}")


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
                token = None

                if hasattr(instance.owner, 'profile') and instance.owner.profile and instance.owner.profile.fcm_token:
                    token = instance.owner.profile.fcm_token
                    print(f"FCM token: {token} (Izoh egasi: {instance.owner.username}")
                else:
                    print(f'Xato: {instance.owner.username} ushun FCM token topilmadi')
                    return
                try:
                    send_push_notification(
                        title='Izoh yuborildi',
                        body=f'{user.username} sizning izohingga like bosdi',
                        token=token,
                        data={
                            "notification_type": "comment_like",
                            "post_id": str(instance.post.id),
                            "comment_id": str(instance.id),
                            "sender_id": str(user.id),
                            "receiver_id": str(instance.owner.id)
                        }
                    )
                    print(f"Bildirishnoma yuborildi: {instance.owner.username} ga")
                except Exception as e:
                    print(f"Xato: Bildirishnoma yuborishda muammo: {e}")



@receiver(post_save,sender=Message)
def create_notification_on_message(sender,instance,created,**kwargs):
    if created and instance.sender != instance.receiver:
        recipient = instance.receiver
        print(f"Xabar qabul qiluvchi: {recipient.userName.username} (ID: {recipient.userName.id})")
        token = getattr(recipient,'fcm_token',None)
        if not token:
            print(f"Xato: {recipient.userName.username} uchun FCM token topilmadi")
            return
        try:
            message_body = instance.message[:50] + '...' if len(instance.message) > 50 else instance.message
            data = {
                    "notification_type":"message",
                    'sender_id': str(instance.receiver.id),
                    'receiver_id': str(instance.sender.id),
            }
            print(f"Sending notification with data: {data}")
            send_push_notification(
                title="Yangi xabar",
                body=f"{instance.sender.userName.username}: {message_body} ",
                token=token,
                data=data
            )
            print(f"Bildirishnoma yuborildi: {recipient.userName.username} ga")
        except Exception as e:
            print(f"Bildirish noima yuborishda xatolik")








# from chat.models import Message
# from django.template.defaultfilters import title
# from .utils import send_notification
# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from django.template.defaulttags import comment
# from django.contrib.auth.models import User
# from fcm.fcm import send_push_notification
# from votes.models import Like
# from notification.models import Notification
# from comments.models import Comment
#
#
#
#
# def send_test_notification(token,title,body):
#     token = "usqfk8ARuKO8znuSbI9_L:APA91bF5OjaakuJQpFRTO_V4aIxvqb-xQ_PKo-0m8rAtt540SZHGxnFVB75vIENxV8F1mzoR8RL2ztMrzDbCOtRSANLo8JSZC7oTQ44aECGbdr6OZ_k96uk"
#     title = "yangilik"
#     body="Bizda yangi mahsulotlar bor!"
#     try:
#         response = send_push_notification(title,body,token)
#         print("✅ Notification yuborildi:", response)
#     except Exception as e:
#         print("❌ Xatolik:", e)
#
#
#
# @receiver(post_save,sender=Like)
# def create_notification_on_like(sender,instance,created,**kwargs):
#     if created and instance.post.owner != instance.user:
#         recipient =  instance.post.owner
#         print(f"Post egasi: {recipient.username} (ID: {recipient.id})")
#         Notification.objects.create(
#             sender=instance.user,
#             receiver=instance.post.owner,
#             post=instance.post,
#             notification_type='like',
#             like=instance
#         )
#         token=None
#         if hasattr(recipient,'profile') and recipient.profile.fcm_token:
#             token = recipient.profile.fcm_token
#             print(f"FCM token{token}(Post Egasi: {recipient.username}) ")
#         else:
#             print(f"Xato: {recipient.username} uchun FCM token topilmadi")
#
#         if token:
#             try:
#                 send_notification(token, 'Yoqtirish', f"{instance.user.username} sizning postingni yoqtirdi")
#                 print(f"Bildirishnoma yuborildi: {receiver.username} ga")
#             except Exception as e:
#                 print(f"Xato: Bildirishnoma yuborishda muammo: {e}")
#
#
#
#
#
# @receiver(post_save,sender=Comment)
# def create_notification_on_comment(sender,instance,created,**kwargs):
#     if not created:
#         return
#
#     if instance.parent:
#         parent_owner = instance.parent.owner
#         if parent_owner != instance.owner:
#             Notification.objects.create(
#                 sender=instance.owner,
#                 receiver=parent_owner,
#                 post=instance.post,
#                 notification_type='reply',
#                 comment=instance
#             )
#             token = None
#             if hasattr(parent_owner,'profile') and parent_owner.profile.fcm_token:
#                 token = parent_owner.profile.fcm_token
#                 print(f"FCM token: {token} (Izoh egasi: {parent_owner.username})")
#             else:
#                 print(f"Xato: {parent_owner.username} uchun FCM token topilmadi")
#
#             if token:
#                 try:
#
#                     send_notification(
#                     token,
#                     title="yangi javob",
#                     body=f"{instance.owner.username} sizning izohingizga jabob berdi"
#                   )
#                     print(f"Bildirishnoma yuborildi: {parent_owner.username} ga")
#                 except Exception as e:
#                     print(f"Xato: Bildirishnoma yuborishda muammo: {e}")
#
#     else:
#         post_owner = instance.post.owner
#         if post_owner != instance.owner:
#             Notification.objects.create(
#                 sender=instance.owner,
#                 receiver=post_owner,
#                 post=instance.post,
#                 notification_type='comment',
#                 comment=instance
#             )
#             token = None
#             if hasattr(post_owner,'profile') and post_owner.profile.fcm_token:
#                 token = post_owner.profile.fcm_token
#                 print(f"FCM token: {token} (Post egasi: {post_owner.username})")
#             else:
#                 print(f"Xato: {post_owner.username} uchun FCM token topilmadi")
#
#             if token:
#                 try:
#                     send_notification(
#                         token,
#                         title="yangi javob",
#                         body=f"{instance.owner.username}sizning postingizga izoh yozdi "
#                     )
#
#                     print(f"Bildirishnoma yuborildi: {post_owner.username} ga")
#                 except Exception as e:
#                     print(f"Xato: Bildirishnoma yuborishda muammo: {e}")
#
#
# @receiver(m2m_changed,sender=Comment.likes.through)
# def create_notification_on_comment_like(sender,instance,action,pk_set,**kwargs):
#     if action == "post_add":
#         for user_id in pk_set:
#             user = User.objects.get(pk=user_id)
#             if instance.owner != user:
#                 Notification.objects.create(
#                     sender=user,
#                     receiver=instance.owner,
#                     post=instance.post,
#                     notification_type='comment_like',
#                     comment=instance
#                 )
#
#                 token = instance.owner.profile.fcm_token if hasattr(instance.post.owner, 'profile') else None
#                 if token:
#                     send_notification(token, 'Yoqtirish', f"{instance.user.username} sizning postingni yoqtirdi")
#
#
# @receiver(post_save,sender=Message)
# def create_notification_on_message(sender,instance,created,**kwargs):
#     if created and instance.sender != instance.receiver:
#         recipient = instance.receiver
#         print(f"Xabar qabul qiluvchi: {recipient.userName.username} (ID: {recipient.userName.id})")
#         token = None
#         if hasattr(recipient,'fcm_token') and recipient.fcm_token:
#             token = recipient.fcm_token
#             print(f"FCM token: {token} (Qabul qiluvchi: {recipient.userName.username})")
#         else:
#             print(f"Xato: {recipient.userName.username} uchun FCM token topilmadi")
#         if token:
#             try:
#                 if instance.type == 'text':
#                     message_body = instance.message[:50] + '...' if len(instance.message) > 50 else instance.message
#                 elif instance.type == 'image':
#                     message_body = 'Rasm yubordi'
#                 elif instance.type == 'video':
#                     message_body = 'Video yubordi'
#                 send_push_notification(
#                     "Yangi xabar",
#                     f"{instance.sender.userName.username}: {message_body}",
#                     token
#                 )
#                 print(f"Bildirishnoma yuborildi: {recipient.userName.username} ga")
#             except Exception as e:
#                 print(f"Bildirish noima yuborishda xatolik")
#
#
#
#
