from posts.serializers import PostSerializer
from .models import UserProfile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    userName = serializers.ReadOnlyField(source="userName.username")
    class Meta:
        model = UserProfile
        fields = ['id', 'userName', 'gender', 'dob', 'phone', 'profileImage','posts']

    def get_posts(self,obj):
        return PostSerializer(obj.userName.posts.all(), many=True).data