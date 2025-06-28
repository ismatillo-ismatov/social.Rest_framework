from urllib.request import build_opener

from rest_framework import serializers
from .models import Post, Story,StoryMessage
from comments.serializers import CommentSerializer
from votes.serializers import LikeSerializer

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    comments = CommentSerializer(many=True,read_only=True)
    likes = LikeSerializer(many=True,read_only=True)

    liked = serializers.SerializerMethodField()
    likeCount = serializers.SerializerMethodField()
    likeId = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id','owner','content','postImage','postVideo','post_date','comments',"likes","liked","likeCount","likeId")

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