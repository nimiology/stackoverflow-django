from django.http import Http404
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS

from Posts.models import Post
from users import models
from authentication.utils import (
    request_wallet,
    check_wallet_id,
    check_token_valid,
    get_token_and_walletid,
)
from users.utils import GetWallet


class CompanyPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        # * Get Token & Wallet_if from request :
        token, wallet_id = get_token_and_walletid(request)

        # * Check wallet with database :
        if check_wallet_id(models.Company, wallet_id):

            # * Check token validations :
            if check_token_valid(token):
                return True
            else:
                return False

        else:
            return False


class EmployeePermission(permissions.BasePermission):

    def has_permission(self, request, view):

        # * Get Token & Wallet_if from request :
        token, wallet_id = get_token_and_walletid(request)
        # * Check wallet with database :
        if check_wallet_id(models.Seller, wallet_id):

            # * Check token validations :
            if check_token_valid(token):
                return True
            else:
                return False
        else:
            return False


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        # * Get Token & Wallet_if from request :
        token, wallet_id = get_token_and_walletid(request)

        # * Check token validations :
        if check_token_valid(token, is_admin=True):
            return True
        else:
            return False


class Update_for_Admin_Get_for_User(permissions.BasePermission):

    def has_permission(self, request, view):

        # * Get Token & Wallet_if from request :
        token, wallet_id = get_token_and_walletid(request)

        if request.method in SAFE_METHODS:
            return True

        elif request.method == "POST":
            if check_token_valid(token, is_admin=True):
                return True

        return False


class Admin_And_User(permissions.BasePermission):

    def has_permission(self, request, view):
        # * Get Token & Wallet_if from request :
        token, wallet_id = get_token_and_walletid(request)

        if check_token_valid(token, is_admin=True) or check_token_valid(token):
            return True

        return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


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


class CheckBan(permissions.BasePermission):
    def has_permission(self, request, view):
        return not GetWallet(request).ban


class CheckBlock(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = GetWallet(request)
        if not (profile in obj.profile.block.all()):
            return True
        else:
            raise ValidationError("You've been blocked!")


class IsItOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile == GetWallet(request)


class IsItPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile == obj.post.profile
