from .models import Like
from rest_framework import serializers
class LikeSerializer(serializers.ModelSerializer):
    like = serializers.ReadOnlyField(source="username")
    # down_vote_by = serializers.ReadOnlyField(source="down_vote_by.username")
    class Meta:
        model = Like
        fields = ["id","post","like","created_at"]