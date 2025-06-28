from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import *
from posts.models import Story
# from  user_profile.serializer import  ProfileSerializer

class ProfileShortSerializer(serializers.ModelSerializer):
    userName = serializers.ReadOnlyField(source="userName.username")
    is_online = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id','userName','profileImage','is_online']



class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileShortSerializer(read_only=True)
    receiver = ProfileShortSerializer(read_only=True)
    # replied_to = serializers.SerializerMethodField()
    replied_to = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(),required=False,allow_null=True)
    file = serializers.SerializerMethodField()
    message = serializers.CharField(required=True,allow_blank=True)

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url

        return None


    class Meta:
        model = Message
        fields = ["id","sender","receiver", "message", "timestamp",'is_read','file','type','replied_to']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.replied_to:
            data['replied_to'] = {
                "id": instance.replied_to.id,
                "message": instance.replied_to.message,
                "sender": {
                    "id": instance.replied_to.sender.id,
                    "userName": instance.replied_to.sender.userName.username,
                    "profileImage":(
                        instance.replied_to.sender.profileImage.url
                        if instance.replied_to.sender.profileImage else None
                    )
                },
                "timestamp": instance.replied_to.timestamp.isoformat()

            }
        else:
            data['replied_to'] = None
        return data




    def create(self, validated_data):

        request = self.context['request']
        sender_profile = request.user.profile
        receiver_id =  request.data.get('receiver')
        receiver_profile = get_object_or_404(UserProfile,id=receiver_id)
        uploaded_file = request.FILES.get('file',None)
        message_type = validated_data.get('type','text')

        if not uploaded_file and not message_type.strip():
            raise serializers.ValidationError("message or file is required")

        if not validated_data.get('type') and uploaded_file:
            content_type = uploaded_file.content_type
            if 'image' in content_type:
                message_type = 'image'
            elif 'video' in content_type:
                message_type = 'video'
            elif 'audio' in content_type:
                message_type = 'audio'
            else:
                message_type = 'file'

        message = Message.objects.create(
            sender=sender_profile,
            receiver=receiver_profile,
            message=validated_data.get('message'),
            file=uploaded_file,
            type=message_type,
            replied_to=validated_data.get('replied_to')
        )
        return message
