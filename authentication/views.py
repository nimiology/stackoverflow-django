from authentication.serializer import (
    DeleteSrializer,
    LoginSrializer,
    RefreshTokenSrializer,
    RegisterSrializer,
    UpdateSrializer,
    FilterSerializer,
)
import requests
from rest_framework import status
from rest_framework.views import APIView
from users import models
from rest_framework import exceptions
import json
from authentication.permission import AdminPermission
from authentication.utils import (
    BASE_AUTH,
    HOST,
    create_obj_by_type,
    get_token,
    get_url_admin_or_user,
    get_url_with_service_and_role,
    send_request_to_server,
)
from rest_framework.response import Response


# * Auth : Get One User object
class GetUser(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = HOST + "/admin/users/" + kwargs["id"]
        return send_request_to_server(url, "get", token=token)


# * Auth : All Users
class AllUser(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = HOST + "/admin/users"
        return send_request_to_server(url=url, request_type="post", token=token)


# * Auth : Register User
class Register(APIView):
    serializer_class = RegisterSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # ! cant register admin
            if kwargs["type"] == "admin":
                raise exceptions.ValidationError(
                    detail="Cant register admin", code=400)

            # * Create url
            url = get_url_with_service_and_role(kwargs["type"], "/register/")

            # * Set auth_basic for acceptable request
            headers = {
                'auth_basic': BASE_AUTH,
            }

            response = requests.post(
                url, dict(serializer.validated_data), headers=headers)
            js_response = response.json()
            if js_response['status'] != False:

                wallet_id = js_response['data']['wallet']['id']
                username = serializer.validated_data['username']

                # ? Create wallet object
                new_wallet = models.Wallet.objects.create(
                    id=wallet_id, username=username)
                new_wallet.save()

                # ? Create user object
                create_obj_by_type(kwargs["type"], new_wallet)
                return Response(response.json(), status=response.status_code)
            else:
                raise exceptions.ValidationError(
                    detail=js_response, code=response.status_code)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Auth : Login User
class Login(APIView):
    serializer_class = LoginSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = get_url_with_service_and_role(kwargs["type"], "/login/")
            return send_request_to_server(url=url, serializer=serializer, request_type="post")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Auth : User Info
class MyInfo(APIView):

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = get_url_admin_or_user(kwargs["type"], "/me")
        return send_request_to_server(url=url, request_type="post", token=token)


# * Auth : Update User Info
class MyInfoUpdate(APIView):
    serializer_class = UpdateSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = get_url_admin_or_user(kwargs["type"], "/me/update")
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Auth : Logout User
class Logout(APIView):

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = get_url_admin_or_user(kwargs["type"], "/logout")
        return send_request_to_server(url=url, request_type="post", token=token)


# * Auth : Delete User
class DeleteAccount(APIView):
    serializer_class = DeleteSrializer

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = HOST + "/delete-my-account"
            token = get_token(request)
            return send_request_to_server(url=url, serializer=serializer, request_type="delete", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Auth : Update Token
class UpdateToken(APIView):
    serializer_class = RefreshTokenSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = HOST + "/update-token"
            return send_request_to_server(url=url, serializer=serializer, request_type="post")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)
