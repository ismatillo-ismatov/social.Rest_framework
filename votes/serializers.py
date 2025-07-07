from .models import Like
from rest_framework import serializers
class LikeSerializer(serializers.ModelSerializer):
    # like = serializers.ReadOnlyField(source="username")
    user = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ["id","post","user","created_at"]


    def get_user(self,obj):
        profile = getattr(obj.user,'profile',None)
        if profile:
            return {
                'id':obj.user.id,
                'userName': profile.userName,
                "profileImage": profile.profileImage.url if profile.profileImage else None
            }
        return {
            'id':obj.user.id,
            'userName':obj.user.username,
            'profileImage':None

        }

