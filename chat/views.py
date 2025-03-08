
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
from twisted.names.root import bootstrap

from user_profile.permissions import IsOwnerReadOnly
from .models import Message
from posts.models import Story
from posts.serializers import StorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .producer import send_message_to_kafka
from .serializers import *
from user_profile.models import UserProfile
from kafka import KafkaProducer
import json

producer =  KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile,userName=self.request.user)
        # user_profile = self.request.user.profile
        return  Message.objects.filter(sender=user_profile) | Message.objects.filter(receiver=user_profile)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print("KElgan DATA: ",data)
        sender_profile = request.user.profile
        receiver_profile = get_object_or_404(UserProfile,id=data['receiver'])

        data['sender'] = sender_profile.id
        data['receiver'] = receiver_profile.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        message_data = serializer.data
        print("KAFKAGA YUBORILDI:",message_data)
        send_message_to_kafka('message_topic',message_data)
        producer.send('messages',value=message_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    @action(detail=False,methods=["get"])
    def get_messages(self,request):
        sender_id = request.query_params.get("sender")
        receiver_id = request.query_params.get("receiver")
        if not sender_id or not receiver_id:
            return  Response({"error":"Sender and receiver must be ID"},status=400)
        sender_profile = get_object_or_404(UserProfile,id=sender_id)
        receiver_profile = get_object_or_404(UserProfile,id=receiver_id)
        messages = Message.objects.filter(sender=sender_profile,receiver=receiver_profile) | Message.objects.filter(sender=receiver_profile,receiver=sender_profile)
        serializer = MessageSerializer(messages,many=True)


        message_data = []
        for message in messages:
            message_data.append({
                'sender': message.sender.userName.username,
                'receiver': message.receiver.userName.username,
                'message': message.message,
                'timestamp': message.timestamp.isoformat(),
            })
        return Response(serializer.data,status=200)



    def update(self, request,*args,**kwargs):
        message = self.get_object()
        partial = kwargs.pop('partial',False)
        serializer = self.get_serializer( message,data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)


