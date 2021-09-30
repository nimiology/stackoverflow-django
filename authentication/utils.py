import jwt
import requests
from users import models
from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist
from decouple import config
from rest_framework.response import Response
from rest_framework import status
import json

# ! Server Information :
HOST = config('HOST')
BASE_AUTH = config('BASE_AUTH')
URL = HOST + "/info"
SERVICE_ID = config('SERVICE_ID')
ROLE_ID_COMPANY = config('ROLE_ID_COMPANY')
ROLE_ID_EMPLOYEE = config('ROLE_ID_EMPLOYEE')


# todo DRY : Sent request and return response to client | data can set in data or serializer
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

        # * for response can't convert to data type
        try:
            j_response = response.json()
        except:
            return Response(response.content, status=response.status_code)

        return Response(j_response, status=response.status_code)

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

        # * for response can't convert to data type
        try:
            j_response = response.json()
        except:
            return Response(response.content, status=response.status_code)

        return Response(j_response, status=response.status_code)

    elif type == "get":

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }
        response = requests.get(url, headers=headers)

        try:
            j_response = response.json()
        except:
            return Response(response.content, status=response.status_code)

        return Response(j_response, status=response.status_code)


# todo DRY : Sent request and return response to client :)
def get_token(request):
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        return token

    # * Cant read Authorization in request header :
    else:
        raise exceptions.ValidationError(detail="ٌCan\'t found Token", code=404)


# todo DRY : Create url ( check ROLE_ID )
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


# todo DRY : Create url ( check type with admin or user )
def get_url_admin_or_user(user_type, main_url):
    # * Check type for roles :
    if user_type == "admin":
        url = HOST + "/admin" + main_url
    elif user_type == "user":
        url = HOST + main_url
    else:
        raise exceptions.ValidationError(detail="Invalid type", code=400)

    return url


# todo Get Request Wallet
def request_wallet(request):
    try:
        token = request.headers['Authorization']

        # * Decode Token for check role
        decoded = jwt.decode(token.split(
            " ")[-1], options={"verify_signature": False})

        wallet_object = models.Wallet.objects.get(id=decoded['wallet_id'])

    # * Cant read Authorization in request header :
    except KeyError:
        raise exceptions.ValidationError(
            detail="ٌCan\'t found Token", code=404)
    except ObjectDoesNotExist:
        raise exceptions.ValidationError(
            detail="ٌInvalid Wallet", code=400)
    except:
        raise exceptions.ValidationError(
            detail="ٌCan\'t decoded Token", code=400)

    return wallet_object


# todo DRY : Check database for user :)
def check_wallet_id(model, wallet_id):
    try:
        wallet_object = model.objects.get(wallet_id=wallet_id)
    except ObjectDoesNotExist:
        # raise exceptions.ValidationError(
        #     detail="ٌYou don't have permission to perform this action", code=400)
        return False
    except:
        raise exceptions.ValidationError(
            detail="ٌCan\'t check Wallet", code=400)

    return True


# todo DRY : Sent request for check token validation :)
def check_token_valid(token, is_admin=False):
    url = URL

    # * Set auth_basic for acceptable request & token ( can be None )
    headers = {
        'auth_basic': BASE_AUTH,
        'Authorization': token,
    }

    if is_admin:
        url = HOST + "/admin/info"

    response = requests.post(url, data={}, headers=headers)

    # * Check token validations
    if response.status_code == 200:
        return True
    else:
        return False


# todo DRY : Get token & wallet_id
def get_token_and_walletid(request):
    try:
        token = request.headers['Authorization']

        # * Decode Token for check role
        decoded = jwt.decode(token.split(
            " ")[-1], options={"verify_signature": False})

        wallet_id = decoded['wallet_id']

    except KeyError:
        raise exceptions.ValidationError(
            detail="ٌCan\'t found Token", code=404)

    # * Cant read Authorization in request header :
    except:
        raise exceptions.ValidationError(
            detail="Invalid Authorization Token", code=401)

    return token, wallet_id
