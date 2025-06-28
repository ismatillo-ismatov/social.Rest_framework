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











