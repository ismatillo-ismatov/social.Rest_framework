from os.path import defpath
from django.contrib.admin import action
from django.contrib.staticfiles.views import serve
from django.utils.termcolors import RESET
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from user_profile.serializer import ProfileSerializer, EditProfileSerializer
from user_profile.models import UserProfile

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes

from posts.models import Post
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerReadOnly
from rest_framework import viewsets,permissions



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        profile = UserProfile.objects.get(userName=request.user)
        serializer = ProfileSerializer(profile,context={'request':request})
        return  Response(serializer.data)


class UserProfileDetailView(APIView):
    def get(self, request,pk):
        try:
            profile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response ({"detail":"Foydalanuvchi topilmadi"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

class EditProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditProfileSerializer

    def get_object(self):
        return self.request.user.profile


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):
    token = request.data.get('fcm_token')
    if not token:
        return Response({'error':'Token is required'},status=400)
    user = request.user
    if not hasattr(user,'profile'):
        return Response({'error':'Profile topilmadi'})
    UserProfile.objects.filter(fcm_token=token).exclude(userName=user).update(fcm_token=None)

    profile = user.profile
    profile.fcm_token = token
    profile.save()
    return  Response({'status':'success','token':token})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_fcm_token(request):
    user = request.user
    if hasattr(user,'profile'):
        user.profile.fcm_token = None
        user.profile.save()
        return Response({'status': 'success', 'message': "Fcm token cleared"})
    return  Response({"error": 'Profile topilmadi'}, status=400)










