from rest_framework import serializers
from .models import Post, Story,StoryMessage
from comments.serializers import CommentSerializer
from votes.serializers import VoteSerializer

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only=True)
    votes = VoteSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ('id','owner','content','post_image','category','post_date','comments',"votes")


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