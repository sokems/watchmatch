from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(name=request.user.id).exists()
