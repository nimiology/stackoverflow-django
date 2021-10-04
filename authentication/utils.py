import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
import json
from decouple import config
import jwt
from users.models import Wallet
from django.core.exceptions import ObjectDoesNotExist


# ! Server Information :
HOST = config('HOST')
AUTH_SECRET_KEY = config('AUTH_SECRET_KEY')
BASE_AUTH = config('BASE_AUTH')
SERVICE_ID = config('SERVICE_ID')
ROLE_ID_COMPANY = config('ROLE_ID_COMPANY')
ROLE_ID_EMPLOYEE = config('ROLE_ID_EMPLOYEE')


# todo : Get Wallet
def get_wallet(token):
    try:
        # * Decode Token
        decoded = jwt.decode(token.split(
            " ")[-1], options={"verify_signature": False})

        wallet_id = decoded['wallet_id']

        wallet_object = Wallet.objects.get(id=wallet_id)

    except ObjectDoesNotExist:
        raise exceptions.ValidationError(
            detail="ٌWallet object not exist", code=400)
    except:
        raise exceptions.ValidationError(
            detail="ٌcan\'n return wallet object", code=400)

    return wallet_object


# todo : Verify token
def verify_token(token):
    try:
        jwt.decode(
            token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except:
        return False

    return True


# todo : Verify token for admin
def verify_token_for_admin(token):
    try:
        data = jwt.decode(
            token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except:
        return False

    if data['role'] == "admin":
        return True
    else:
        return False


# todo : Sent request and return response to client | requests data can set in data or serializer
def send_request_to_server(url, type, serializer=None, token=None, data_type=None, data={}):

    if type == "post":

        # * for post method without serializer
        if not serializer == None:
            data = dict(serializer.validated_data)

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }

        # ! for request with nested datetime's object can't use data and should use json
        if data_type == "json":
            response = requests.post(url, json=data, headers=headers)
        elif data_type == "files":
            response = requests.post(url, files=data, headers=headers)
        else:
            response = requests.post(url, data=data, headers=headers)

        return Response(response.json(), status=response.status_code)

    elif type == "delete":

        # * for post method without serializer
        if not serializer == None:
            data = dict(serializer.validated_data)

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }
        response = requests.delete(url, json=data, headers=headers)

        return Response(response.json(), status=response.status_code)

    elif type == "get":

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }
        response = requests.get(url, headers=headers)

        return Response(response.json(), status=response.status_code)


# todo : Get token
def get_token(request):
    if 'Authorization' in request.headers:
        return request.headers['Authorization'].split(" ")[-1]
    else:
        raise exceptions.ValidationError(
            detail="ٌCan\'t found Token", code=404)


# todo : Create url ( with ROLE_ID )
def get_url_with_service_and_role(user_type, main_url):
    # * Check type for roles :
    if user_type == "company":
        url = HOST + main_url + ROLE_ID_COMPANY + "/" + SERVICE_ID
    elif user_type == "employee":
        url = HOST + main_url + ROLE_ID_EMPLOYEE + "/" + SERVICE_ID
    elif user_type == "admin":
        url = HOST + "/admin" + main_url
    else:
        raise exceptions.ValidationError(detail="Invalid type", code=400)

    return url


# todo DRY : Create url for login ( admin or user )
def get_url_admin_or_user(user_type, main_url):

    # * Check type for roles :
    if user_type == "admin":
        url = HOST + "/admin" + main_url
    elif user_type == "user":
        url = HOST + main_url
    else:
        raise exceptions.ValidationError(detail="Invalid type", code=400)

    return url
