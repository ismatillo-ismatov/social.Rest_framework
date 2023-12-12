from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import viewsets
from user_profile.permissions import IsOwnerReadOnly
from .models import Message
from posts.models import Story
from posts.serializers import StorySerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import *



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    def post(request,sender=None ,receiver=None):
        if request.method == "GET":
            messages = Message.objects.filter(sender_id=sender,receiver_id=receiver,is_read=False)
            serializer = MessageSerializer(messages,many=True, context={"request":request})
            for message in messages:
                message.is_read = True
                message.save()
            return JsonResponse(serializer.data,safe=False)
        elif request.method == "POST":
            data = JSONParser().parse(request)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors,status=400)

    def message_view(self,request,sender,receiver):
        if request.method == "GET":
            return render(request,{'users':User.objects.exclude(username=request.user.username),
                                   'receive':User.objects.get(id=receiver),
                                   'messages': Message.objects.filter(sender_id=sender,receiver_id=receiver)|
                                   Message.objects.filter(sender_id=receiver,receiver_id=sender)
                                   })



    def update(self, request, pk=None):
        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

# class StoryMessage(viewsets.ModelViewSet):
#     queryset = Story.objects.all()
#     serializer_class = StorySerializer
#     permission_classes = [IsAuthenticated]
#
#
#     def story_message(self,request,sender,receiver):
#         if request.method == "GET":
#             return render(request,{'users':User.objects.exclude(username=request.user.username),
#                                 'receive':User.objects.get(id=receiver),
#                                 'message':  Story.objects.filter(sender_id=receiver,receiver=sender)
#                                    })