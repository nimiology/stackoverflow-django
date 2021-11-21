from Posts.models import Post
from django.http import Http404
from rest_framework.exceptions import ValidationError
from users.utils import (
    GetWallet,
    VerifyToken,
)
from rest_framework import permissions


# Is he owner of the object?
class IsAuthenticate(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(GetWallet(request))


class MediaOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = GetWallet(request)
        if obj.post:
            return obj.post.profile == user
        elif obj.question:
            return obj.question.profile == user
        elif obj.answer:
            return obj.answer.profile == user


class IsItOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile == GetWallet(request)


class DeleteObjectByAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.profile == GetWallet(request):
            return True
        else:
            if 'Authorization' in request.headers:
                return VerifyToken(request.headers['Authorization'])['role'] == 'admin' or obj.profile == GetWallet(
                    request)
            else:
                raise ValidationError('There is no Token!')


# Is he owner of the post of the object?
class IsItPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return GetWallet(request) == obj.post.profile


# Is the user admin
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'Authorization' in request.headers:
            return VerifyToken(request.headers['Authorization'])['role'] == 'admin'
        else:
            raise ValidationError('There is no Token!')


class IsRequestMethodPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
