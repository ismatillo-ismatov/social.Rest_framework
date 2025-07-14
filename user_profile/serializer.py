from rest_framework.fields import SerializerMethodField

from chat.models import Message
from chat.serializers import MessageSerializer
from posts.serializers import PostSerializer
# from users.serializer import UserSerializer
from .models import UserProfile
from rest_framework import serializers








class ProfileSerializer(serializers.ModelSerializer):
    is_online = serializers.BooleanField(read_only=True)
    last_activity = serializers.DateTimeField(read_only=True)
    posts = serializers.SerializerMethodField()
    messages = SerializerMethodField()
    userName = serializers.ReadOnlyField(source="userName.username")
    class Meta:
        model = UserProfile
        fields = ['id', 'userName', 'gender', 'dob', 'phone', 'profileImage','is_online','last_activity','posts','messages','fcm_token']

    def get_posts(self,obj):
        return PostSerializer(obj.userName.posts.all(), many=True,context=self.context).data



    def get_messages(self,obj):
        messages = Message.objects.filter(sender=obj,) | Message.objects.filter(receiver=obj)
        return MessageSerializer(messages,many=True).data



class EditProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True,required=False)
    class Meta:
        model = UserProfile
        fields = ['username','gender','profileImage','bio']

    def update(self, instance, validated_data):
        username = validated_data.pop('username',None)
        if username:
            print("⚙️ Username update requested:", username)
            user = instance.userName
            print("👤 Old username:", user.username)
            user.username = username
            user.save()
            print("✅ Username updated:", user.username)
        return  super().update(instance,validated_data)