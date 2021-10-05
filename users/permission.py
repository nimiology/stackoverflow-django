from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from users.utils import GetWallet, GetCompany


class IsItOwnerCompany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = GetWallet(request)
        """Get Company"""
        company = GetCompany(profile)
        if obj.company == company:
            return True
        else:
            raise ValidationError('access denied')
