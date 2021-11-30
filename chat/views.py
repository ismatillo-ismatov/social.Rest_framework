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

# @csrf_exempt
# def user_list(request,pk=None):
#     if request.method == "GET":
#         if pk:
#             users = User.objects.filter(id=pk)
#         else:
#             users = User.objects.all()
#         serializer = UserSerializer(users,many=True,context={"request":request})
#         return JsonResponse(serializer.data,safe=False)
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data,status=201)
#         return JsonResponse(serializer.errors,status=400)


# @csrf_exempt
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]
    def post(request, receiver=None):
        if request.method == "GET":
            messages = Message.objects.filter(receiver_id=receiver)
            serializer = MessageSerializer(messages,many=True, context={"request":request})
            return JsonResponse(serializer.data,safe=False)
        elif request.method == "POST":
            data =  JSONParser().parse(request)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors,status=400)
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)