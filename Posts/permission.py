from Posts.models import Post
from django.http import Http404
from rest_framework.exceptions import ValidationError
from users.utils import (
    GetWallet,
    VerifyToken,
)
from rest_framework import permissions


# is he already blocked by Post owner?
class BlockedByUserWithPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            try:
                postOwner = Post.objects.get(slug=view.kwargs['slug']).profile
            except Post.DoesNotExist:
                raise Http404
            if not (GetWallet(request) in postOwner.block.all()):
                return True
            else:
                raise ValidationError("You've been blocked")

        return request.method != 'GET'


class IsPrivateWithPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            try:
                obj = Post.objects.get(slug=view.kwargs['slug']).profile
            except Post.DoesNotExist:
                raise Http404
            requestOwner = GetWallet(request)
            if obj.profile.private:
                if GetWallet(request) != requestOwner:
                    if obj.profile in requestOwner.following.all():
                        return True
                    else:
                        raise ValidationError('This page is private')
                else:
                    return True
            else:
                return True
        return request.method != 'GET'


class IsPrivate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        requestOwner = GetWallet(request)
        if obj.profile.private:
            if requestOwner != obj.profile:
                if obj.profile in requestOwner.following.all():
                    return True
                else:
                    raise ValidationError('This page is private')
            else:
                return True
        else:
            return True


# is he already blocked by owner?
class CheckBlock(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = GetWallet(request)
        if not (profile in obj.profile.block.all()):
            return True
        else:
            raise ValidationError("You've been blocked!")


# Is he owner of the object?
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


# Is the request method Delete?
class IsRequestMethodDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'DELETE'


class IsRequestMethodPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
