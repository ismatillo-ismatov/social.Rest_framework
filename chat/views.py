from importlib.metadata import files

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.status import HTTP_400_BAD_REQUEST
from twisted.names.root import bootstrap
from urllib3 import request

from user_profile.permissions import IsOwnerReadOnly
from .models import Message
from posts.models import Story
from posts.serializers import StorySerializer
from rest_framework.permissions import IsAuthenticated
import redis
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from .serializers import *
from user_profile.models import UserProfile
import json
from collections import defaultdict

redis_client = redis.StrictRedis(host='localhost',port=6379,db=0)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]


    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile,userName=self.request.user)
        return  Message.objects.filter(sender=user_profile) | Message.objects.filter(receiver=user_profile)

    @action(detail=False,methods=["post"],url_path='mark_as_read',parser_classes=[JSONParser])
    def mark_as_read(self,request):
        sender_id = request.data.get("sender")
        receiver_id = request.data.get("receiver")
        if not sender_id or not  receiver_id:
            return Response({"error":"Sender and receiver requited"},status=status.HTTP_400_BAD_REQUEST)
        sender = get_object_or_404(UserProfile,id=sender_id)
        receiver = get_object_or_404(UserProfile,id=receiver_id)

        current_user_profile = request.user.profile
        if current_user_profile != receiver:
            return Response({"error":"faqat oluvchi xabarlarni oqilgan deb belgilay olasiz"},status=status.HTTP_403_FORBIDDEN)
        messages = Message.objects.filter(sender=sender,receiver=receiver,is_read=False)
        messages.update(is_read=True)
        return Response({"status":"Xabar oqilgan deb belgiyandi"},status=200)

    @action(detail=False,methods=['post'],url_path='mark_all_as_read')
    def mark_all_ass_read(self,request):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')

        if not sender_id or not receiver_id:
            return Response({"error": "Sender va Receiver ID kerak"},status=400)
        current_user_profile = request.user.profile
        unread_message = Message.objects.filter(
            sender__id=sender_id,
            receiver_id=current_user_profile,
            is_read=False
        )

        count = unread_message.update(is_read=True)
        return Response({"status": f"{count} ta xabar oqilgab deb belgilandi"},status=200)

    @action(detail=False,methods=['get'],url_path='inbox')
    def inbox(self,request):
        current_user_profile = request.user.profile
        all_messages = Message.objects.filter(
            sender=current_user_profile
        ) | Message.objects.filter(
            receiver=current_user_profile
        )

        conversations = {}
        for msg in all_messages.order_by('timestamp'):
            if msg.sender == current_user_profile:
                contact = msg.receiver
            else:
                contact = msg.sender

            conversations[contact.id] = msg

        serializer = MessageSerializer(conversations.values(), many=True)
        return Response(serializer.data,status=200)

    def create(self, request, *args, **kwargs):
        print("Kelayotgan ma'lumot:", request.data)
        uploaded_file = request.FILES.get('file',None)
        message_type = request.data.get('type','text')

        content_type = uploaded_file.content_type if uploaded_file else None
        if not request.data.get('type'):
            if content_type:
                if 'image' in content_type:
                    message_type = 'image'
                elif 'video' in content_type:
                    message_type = 'video'
                elif 'audio' in content_type:
                    message_type = 'audio'
                else:
                    message_type = 'file'
            else:
                message_type = 'text'

        mutable_data = request.data.copy()
        mutable_data['type'] = message_type

        serializer = self.get_serializer(data=mutable_data,context={'request':request})
        if not serializer.is_valid():
            print("Xatolik:", serializer.errors)
            return Response(serializer.errors,status=400)
        serializer.save()


        message_data = serializer.data


        redis_client.publish('chat_channel',json.dumps(message_data))
        print("Redisga yuborildi:",message_data)

        return Response(serializer.data,status=status.HTTP_201_CREATED)


    @action(detail=False, methods=["get"])
    def get_messages(self, request):
        sender_id = request.query_params.get("sender")
        receiver_id = request.query_params.get("receiver")
        if not sender_id or not receiver_id:
            return Response({"error": "Sender and receiver must be ID"}, status=400)
        sender_profile = get_object_or_404(UserProfile, id=sender_id)
        receiver_profile = get_object_or_404(UserProfile, id=receiver_id)
        current_user_profile = request.user.profile
        if current_user_profile != sender_profile and current_user_profile !=receiver_profile:
            return Response({"error":"Siz ushbu suhbatni korishga  ruxsatga ega emassiz"}, status=403)

        messages = Message.objects.filter(sender=sender_profile, receiver=receiver_profile) | Message.objects.filter(
            sender=receiver_profile, receiver=sender_profile)
        serializer = MessageSerializer(messages, many=True)

        message_data = []
        for message in messages:
            message_data.append({
                'sender': message.sender.userName.username,
                'receiver': message.receiver.userName.username,
                'message': message.message,
                'timestamp': message.timestamp.isoformat(),
            })
        return Response(serializer.data, status=200)




    def update(self, request,*args,**kwargs):
        message = self.get_object()
        partial = kwargs.pop('partial',False)
        serializer = self.get_serializer( message,data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)


