from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from users import models
from authentication.utils import (
    request_wallet,
    check_wallet_id,
    check_token_valid,
    get_token_and_walletid,
)


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


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
