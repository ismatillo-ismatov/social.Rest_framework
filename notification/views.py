from django.dispatch import receiver
from  rest_framework import generics,permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import status
from django.contrib.auth import get_user_model

from .utils import send_notification

from .signals import send_test_notification



# Create your views here.

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request,pk):
    try:
        notification = Notification.objects.get(pk=pk,receiver=request.user)
        notification.is_read = True
        notification.save()
        return Response({"messaage":"Notification marked as read"})
    except Notification.DoesNotExist:
        return Response({'error':'Notification not found'})


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(receiver=user).order_by('-created_at')



class SendFCMNotificationView(APIView):
    def post(self,request):
        token = request.data.get('token')
        title = request.data.get('title')
        body = request.data.get('body')

        if not token or not title or not body:
            return Response({'error': "need token, title, body"},status=status.HTTP_400_BAD_REQUEST)
        try:
            send_test_notification(token,title,body)
            return Response({"success":"send to notification"})
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
