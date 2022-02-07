from rest_framework.exceptions import ValidationError
from rest_framework import permissions


class IsItOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile == request.user
