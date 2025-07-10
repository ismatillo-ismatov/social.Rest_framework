<<<<<<< HEAD
import firebase_admin
from firebase_admin import credentials, messaging
import os

# Faqat bir marta initialize qilish uchun flag
firebase_app = None

def initialize_firebase():
    global firebase_app
    if not firebase_app:
        cred_path = os.path.join(os.path.dirname(__file__), 'service_account.json')
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)

def send_push_notification(title, body, token):
    initialize_firebase()

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token
    )
    response = messaging.send(message)
    return response
=======
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
>>>>>>> e6d0bccbf2cc5ba26476fb64e4b90886ede60e94
