from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User

class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  = ('id','username',)

class CommentSerializer(serializers.ModelSerializer):
    owner = ShortUserSerializer(read_only=True)
    ownerProfileImage = serializers.SerializerMethodField()
    ownerUserName = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id','owner','post','parent', 'comment',
                  'comment_image','comment_date','ownerUserName',
                  'ownerProfileImage','replies','like_count', 'is_liked']
        extra_kwargs = {
        'post':{'required':False}
        }

    def get_ownerUserName(self,obj):
        if hasattr(obj.owner,'profile') and obj.owner.profile.userName:
            return str(obj.owner.profile.userName)
        return None

    def get_ownerProfileImage(self,obj):
        if hasattr(obj.owner,'profile') and obj.owner.profile.profileImage:
            return obj.owner.profile.profileImage.url
        return  None



    def get_replies(self,obj):
        replies = obj.replies.all()
        print(f"Reply for comment{obj.id}:{replies}")
        return ReplySerializer(replies, many=True,context=self.context).data


    def get_is_liked(self,obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False

    def get_like_count(self,obj):
        return obj.likes.count()

class ReplySerializer(serializers.ModelSerializer):
    owner = ShortUserSerializer(read_only=True)
    ownerProfileImage = serializers.SerializerMethodField()
    ownerUserName = serializers.SerializerMethodField()


    class Meta:
        model = Comment
        fields = ['id','comment','owner','ownerProfileImage','ownerUserName','comment_date']

    def get_ownerUserName(self,obj):
        if hasattr(obj.owner,'profile') and obj.owner.profile.userName:
            return str(obj.owner.profile.userName)
        return None

    def get_ownerProfileImage(self,obj):
        if hasattr(obj.owner,'profile') and obj.owner.profile.profileImage:
            return obj.owner.profile.profileImage.url
        return None