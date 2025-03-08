from rest_framework.fields import SerializerMethodField

from chat.models import Message
from chat.serializers import MessageSerializer
from posts.serializers import PostSerializer
# from users.serializer import UserSerializer
from .models import UserProfile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    messages = SerializerMethodField()
    # userName = UserSerializer()
    userName = serializers.ReadOnlyField(source="userName.username")
    # userName = serializers.CharField(source="username")
    class Meta:
        model = UserProfile
        fields = ['id', 'userName', 'gender', 'dob', 'phone', 'profileImage','posts','messages',]

    def get_posts(self,obj):
        return PostSerializer(obj.userName.posts.all(), many=True).data


    def get_messages(self,obj):
        messages = Message.objects.filter(sender=obj,) | Message.objects.filter(receiver=obj)
        return MessageSerializer(messages,many=True).data

    # def get_messages(self,obj):
    #     user = obj.userName
    #     messages = Message.objects.filter(sender=user,) | Message.objects.filter(receiver=user)
    #     return MessageSerializer(messages,many=True).data