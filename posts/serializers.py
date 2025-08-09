from asyncio import gather

from rest_framework import serializers

from user_profile.miniProfile_serializer  import MiniProfileSerializer
from .models import Post, Story,StoryMessage
from comments.serializers import CommentSerializer
from votes.serializers import LikeSerializer

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    # owner = MiniProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True,read_only=True)
    likes = LikeSerializer(many=True,read_only=True)
    liked = serializers.SerializerMethodField()
    likeCount = serializers.SerializerMethodField()
    likeId = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id','owner','content','postImage','postVideo','post_date','comments',"likes","liked","likeCount","likeId")


    def get_owner(self,obj):
        profile = getattr(obj.owner,'profile',None)
        request = self.context.get('request')
        return {
            'id': obj.owner.id,
            'profile_id': profile.id if profile else None,
            'username': profile.userName.username if profile else obj.owner.username,
            'profileImage': request.build_absolute_uri(profile.profileImage.url) if request and profile and  profile.profileImage else None
        }





    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.postImage.url
            if not url.startswith('http'):
                return request.build_absolute_url(url)
            return  url

    def get_video_url(self,obj):
        request = self.context.get('request')
        if obj.postVideo:
            return request.build_absolute_uri(obj.postVideo.url)
        return None

    def get_liked(self,obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.votes.filter(user=request.user).exists()
        return False



    def get_likeCount(self,obj):
        return obj.votes.count()

    def get_likeId(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            like = obj.votes.filter(user=request.user).first()
            return like.id if like else None
        return None





class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ['id','title', 'story','story_date']
        read_only_fields = ["owner"]

    def create(self,validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)



class StoryMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryMessage
        fields = ('id','sender','recipient','story','message','created_date')