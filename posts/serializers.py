from rest_framework import serializers
from .models import Post, Story,StoryMessage
from comments.serializers import CommentSerializer
from votes.serializers import LikeSerializer

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    comments = CommentSerializer(many=True,read_only=True)
    likes = LikeSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ('id','owner','content','postImage','post_date','comments',"likes",)

    def get_image_url(self,obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_obsolute_uri(obj.image.url)
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