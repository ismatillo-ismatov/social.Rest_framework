from user_profile.serializer import ProfileSerializer
from user_profile.models import UserProfile
from django.shortcuts import render
from .permissions import IsOwnerReadOnly
from rest_framework import viewsets,permissions


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)