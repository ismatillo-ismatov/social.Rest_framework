class ReplySerializer(serializers.ModelSerializer):
    owner = ShortUserSerializer(read_only=True)
    ownerProfileImage = serializers.SerializerMethodField()
    ownerUserName = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'owner', 'ownerProfileImage', 'ownerUserName', 'comment_date']

    def get_ownerUserName(self, obj):
        if hasattr(obj.owner, 'profile') and obj.owner.profile.userName:
            return str(obj.owner.profile.userName)
        return None

    def get_ownerProfileImage(self, obj):
        if hasattr(obj.owner, 'profile') and obj.owner.profile.profileImage:
            return obj.owner.profile.profileImage.url
        return None
