from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS

from users.utils import GetCompany


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsItOwnerCompany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = request.user
        """Get Company"""
        company = GetCompany(profile)
        if obj.company == company:
            return True
        else:
            raise ValidationError('access denied')
