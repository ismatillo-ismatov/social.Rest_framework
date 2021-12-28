from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework import viewsets
from user_profile.permissions import IsOwnerReadOnly
from .models import Message
from .serializers import *

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]
    def post(request,sender=None ,receiver=None):
        if request.method == "GET":
            messages = Message.objects.filter(sender_id=sender,receiver_id=receiver)
            serializer = MessageSerializer(messages,many=True, context={"request":request})
            return JsonResponse(serializer.data,safe=False)
        elif request.method == "POST":
            data = JSONParser().parse(request)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors,status=400)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)