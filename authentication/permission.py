from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from users import models
from authentication.utils import (
    get_token,
    get_wallet,
    verify_token,
    verify_token_for_admin,
)


class CompanyPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        token = get_token(request)

        if verify_token(token):
            wallet = get_wallet(token)

            return models.Company.objects.filter(profile=wallet).exists()

        else:
            return False


class EmployeePermission(permissions.BasePermission):

    def has_permission(self, request, view):

        token = get_token(request)

        if verify_token(token):
            wallet = get_wallet(token)

            return models.Employee.objects.filter(profile=wallet).exists()

        else:
            return False


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
            token = get_token(request)
            if verify_token(token):
                wallet = get_wallet(token)
                print(obj.profile)
                print(wallet)
                return obj.profile == wallet
            else:
                return False
