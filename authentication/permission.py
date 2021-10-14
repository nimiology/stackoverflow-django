from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from users import models
from authentication.utils import get_token, get_wallet, get_wallet_and_verify_token, verify_token, verify_token_for_admin, verify_token_for_user


class CompanyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        wallet = get_wallet_and_verify_token(request=request)
        return models.Company.objects.filter(profile=wallet).exists()


class EmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        wallet = get_wallet_and_verify_token(request=request)
        return models.Employee.objects.filter(profile=wallet).exists()


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        token = get_token(request)
        return verify_token_for_admin(token)


class AdminOrUserReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        token = get_token(request)
        if request.method in SAFE_METHODS:
            return True
        else:
            return verify_token_for_admin(token)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class OwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            wallet = get_wallet_and_verify_token(request=request)
            return obj.profile == wallet


class Admin_And_User(permissions.BasePermission):
    def has_permission(self, request, view):
        token = get_token(request)
        if verify_token_for_admin(token) or verify_token_for_user(token):
            return True
        return False
