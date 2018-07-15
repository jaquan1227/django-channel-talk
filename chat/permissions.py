from rest_framework import permissions
from django.db.models.query import EmptyQuerySet

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsRoomMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user.filter(nickname=request.user):
            return True
        return False

class IsSameUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
