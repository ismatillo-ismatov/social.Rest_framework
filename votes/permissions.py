from rest_framework import permissions

class VoteReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.up_vote_by == request.user or obj.down_vote_by==request.user